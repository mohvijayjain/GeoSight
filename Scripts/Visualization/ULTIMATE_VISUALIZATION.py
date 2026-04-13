import rasterio
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import frangi, unsharp_mask
from skimage.morphology import thin, remove_small_objects, binary_closing, disk, binary_dilation, remove_small_holes, binary_opening
from skimage.exposure import rescale_intensity, adjust_gamma
import sknw
import os

# --- PATHS ---
PRED_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\GeoSight_Final_Predictions"
IMG_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\GeoSight_Consolidated_Dataset\Images"
OUTPUT_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\GEOSIGHT_SIGNATURE_RESULTS"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# YOUR FULL 40 CHAMPION TILES
FILES = [
    "Delhi_tile_1182_pred.tif", "Delhi_tile_1181_pred.tif", "Delhi_tile_1183_pred.tif",
    "Delhi_tile_1184_pred.tif", "Delhi_tile_1140_pred.tif", "Delhi_tile_136_pred.tif",
    "Delhi_tile_1141_pred.tif", "Delhi_tile_703_pred.tif", "Delhi_tile_704_pred.tif",
    "Delhi_tile_283_pred.tif", "Delhi_tile_178_pred.tif", "Delhi_tile_326_pred.tif",
    "Delhi_tile_179_pred.tif", "Delhi_tile_1225_pred.tif", "Delhi_tile_368_pred.tif",
    "Delhi_tile_1224_pred.tif", "Delhi_tile_1226_pred.tif", "Delhi_tile_325_pred.tif",
    "Delhi_tile_1139_pred.tif", "Delhi_tile_240_pred.tif", "Haryana_tile_15199_pred.tif",
    "Haryana_tile_15378_pred.tif", "Haryana_tile_15379_pred.tif", "Haryana_tile_15291_pred.tif",
    "Haryana_tile_15382_pred.tif", "Haryana_tile_15474_pred.tif", "Haryana_tile_15472_pred.tif",
    "Haryana_tile_15200_pred.tif", "Haryana_tile_15473_pred.tif", "Haryana_tile_15381_pred.tif",
    "Haryana_tile_15290_pred.tif", "Haryana_tile_15380_pred.tif", "Haryana_tile_15289_pred.tif",
    "Haryana_tile_15471_pred.tif", "Haryana_tile_7834_pred.tif", "Haryana_tile_15470_pred.tif",
    "Haryana_tile_15110_pred.tif", "Haryana_tile_7832_pred.tif", "Haryana_tile_7830_pred.tif",
    "Haryana_tile_15201_pred.tif"
]

def compute_graph_quality_metrics(G, resolution_m_per_px, tile_area_m2):
    import networkx as nx
    MIN_CONNECTIVITY      = 0.70   # >70% nodes in one connected component
    MIN_ROAD_DENSITY      = 500.0  # >500m of road per km² (urban tile minimum)
    MAX_DEAD_END_RATIO    = 0.35   # <35% of nodes are dead ends

    nodes = list(G.nodes())
    total_nodes = len(nodes)
    if total_nodes == 0:
        return {
            'connectivity': 0.0,
            'total_road_length_m': 0.0,
            'road_density_m_per_km2': 0.0,
            'dead_end_ratio': 0.0,
            'passed': False,
            'status': "FAILED"
        }

    components = list(nx.connected_components(G))
    largest_comp_size = len(max(components, key=len)) if components else 0
    connectivity = largest_comp_size / total_nodes

    total_length_m = 0.0
    for u, v in G.edges():
        total_length_m += edge_length_meters(G, u, v, resolution_m_per_px)

    tile_area_km2 = tile_area_m2 / 1_000_000.0
    road_density = total_length_m / tile_area_km2 if tile_area_km2 > 0 else 0

    dead_ends = sum(1 for n in nodes if G.degree(n) == 1)
    dead_end_ratio = dead_ends / total_nodes

    passed = (connectivity >= MIN_CONNECTIVITY) and (road_density >= MIN_ROAD_DENSITY) and (dead_end_ratio <= MAX_DEAD_END_RATIO)

    return {
        'connectivity': round(connectivity, 3),
        'total_road_length_m': round(total_length_m, 1),
        'road_density_m_per_km2': round(road_density, 1),
        'dead_end_ratio': round(dead_end_ratio, 3),
        'passed': passed,
        'status': "PASSED" if passed else "FAILED"
    }

def get_frangi_sigmas(resolution_m_per_px):
    """
    Sigmas are derived from physical road widths in meters divided by 2x the GSD. 
    Never hardcode these values.
    """
    arterial_sigma = round(20 / (2 * resolution_m_per_px), 1)
    highway_sigma = round(35 / (2 * resolution_m_per_px), 1)
    trunk_sigma = round(55 / (2 * resolution_m_per_px), 1)
    return (arterial_sigma, highway_sigma, trunk_sigma)

def is_boundary_node(node_coords, image_shape, buffer_px=5):
    r, c = node_coords
    max_r, max_c = image_shape[0], image_shape[1]
    if r <= buffer_px or r >= max_r - buffer_px:
        return True
    if c <= buffer_px or c >= max_c - buffer_px:
        return True
    return False

def edge_length_meters(G, u, v, resolution_m_per_px):
    # sknw can sometimes return MultiGraphs (0 key), handle both gracefully
    edge_data = G[u][v][0] if 0 in G[u][v] else G[u][v]
    if 'pts' not in edge_data:
        return 0.0
    pts = edge_data['pts']
    if len(pts) < 2:
        return 0.0
    diffs = np.diff(pts, axis=0) # [N-1, 2]
    dist_px = np.sum(np.linalg.norm(diffs, axis=1))
    return dist_px * resolution_m_per_px

def prune_major_road_graph(G, resolution_m_per_px, image_shape):
    import networkx as nx
    changed = True
    while changed:
        changed = False
        nodes = list(G.nodes())
        for n in nodes:
            if G.degree(n) == 1:
                node_coords = G.nodes[n]['o']
                if is_boundary_node(node_coords, image_shape):
                    continue
                
                neighbor = list(G.neighbors(n))[0]
                length_m = edge_length_meters(G, n, neighbor, resolution_m_per_px)
                if length_m < 150.0:
                    G.remove_node(n)
                    changed = True
                    
    # Disconnected component pruning
    components = list(nx.connected_components(G))
    for comp in components:
        comp_subgraph = G.subgraph(comp)
        total_length_m = 0.0
        # MultiGraph / Graph safe iteration
        for u, v in comp_subgraph.edges():
            total_length_m += edge_length_meters(G, u, v, resolution_m_per_px)
            
        if total_length_m < 500.0:
            G.remove_nodes_from(comp)
            
    return G

def clean_urban_mask(urban_mask, resolution_m_per_px):
    """
    Cleans the raw urban prediction mask to eliminate noise and minor alleyways.
    Runs Opening FIRST to destroy thin structures, then rigorously closes massive gaps.
    """
    # 1. Aggressive Opening FIRST: Annihilates thin alleyways and noise (~20m radius)
    opening_radius = int(20 / resolution_m_per_px) 
    mask = binary_opening(urban_mask, disk(opening_radius))
    
    # 2. Small object removal: Kills isolated chunks
    min_size_px = int(8000 / (resolution_m_per_px ** 2)) 
    mask = remove_small_objects(mask, min_size=min_size_px)
    
    # 3. Massive Closing: Bridges massive gaps (up to 80m) snapped by the Opening
    closing_radius = int(80 / resolution_m_per_px) 
    mask = binary_closing(mask, disk(closing_radius))
    
    # 4. Hole filling: Complete the solid blocks
    hole_threshold_px = int(10000 / (resolution_m_per_px ** 2))
    mask = remove_small_holes(mask, area_threshold=hole_threshold_px)
    
    return mask

def generate_signature_outputs():
    print(f"💎 Generating Signature Audit for {len(FILES)} tiles...")
    all_metrics = []
    
    for f in FILES:
        try:
            mask_path = os.path.join(PRED_DIR, f)
            orig_path = os.path.join(IMG_DIR, f.replace("_pred.tif", ".tif"))

            with rasterio.open(mask_path) as src: mask = src.read(1)
            with rasterio.open(orig_path) as src:
                orig = src.read([3, 2, 1]).transpose(1, 2, 0)
                
                # --- STEP 1: ADVANCED PHOTO EDITING ---
                # Normalize and apply Unsharp Mask (Sharpening)
                img_norm = np.clip(orig / 2200.0, 0, 1)
                sharpened = unsharp_mask(img_norm, radius=1, amount=1.5)
                
                # Contrast Stretching & Gamma Correction (Your request for better clarity)
                p2, p98 = np.percentile(sharpened, (2, 98))
                img_rescaled = rescale_intensity(sharpened, in_range=(p2, p98))
                final_bg = adjust_gamma(img_rescaled, 1.3) # Darkened for Neon contrast

            # --- STEP 2: MASK SURGERY (LAYER 1) ---
            raw_urban = (mask == 2).astype(bool)
            RESOLUTION_M_PER_PX = 10.0
            roads_clean = clean_urban_mask(raw_urban, RESOLUTION_M_PER_PX)

            # --- STEP 2.5: FRANGI VESSEL EXTRACTION ---
            roads_raw_float = roads_clean.astype(float)
            
            # Calculate physical sigmas 
            sigmas = get_frangi_sigmas(RESOLUTION_M_PER_PX)
            if FILES.index(f) == 0:
                print(f"[GeoSight] Frangi sigmas computed: arterial={sigmas[0]}, highway={sigmas[1]}, trunk={sigmas[2]} (res={RESOLUTION_M_PER_PX}m/px)")
            
            # Frangi filter specifically enhances continuous "vessel-like" lines
            road_vessels = frangi(roads_raw_float, sigmas=sigmas, black_ridges=False)
            
            # Thresholding the vessels
            binary = road_vessels > (np.mean(road_vessels) + 1.5 * np.std(road_vessels))
            
            # --- STEP 3: MORPHOLOGICAL RECONSTRUCTION ---
            clean = remove_small_objects(binary, min_size=120)
            # Bridge gaps with a large radius to ensure connectivity
            clean = binary_closing(clean, disk(6))
            # Slight dilation to ensure a solid skeleton
            clean = binary_dilation(clean, disk(1))

            skeleton = thin(clean)

            # --- STEP 4: TRIPLE-PANEL SIGNATURE VIEW ---
            fig, axes = plt.subplots(1, 3, figsize=(27, 9), facecolor='#0a0a0a')
            
            # Panel 1: Deep-Contrast Satellite
            axes[0].imshow(final_bg)
            axes[0].set_title(f"Enhanced Satellite ({f.split('_')[0]})", color='cyan', fontsize=20, pad=20)
            
            # Panel 2: Multi-Class Segmentation (Overlaid)
            axes[1].imshow(final_bg, alpha=0.8)
            axes[1].imshow(mask, cmap='terrain', alpha=0.45)
            axes[1].set_title("GeoSight Neural Segmentation", color='cyan', fontsize=20, pad=20)
            
            # Panel 3: Neon Infrastructure Audit
            axes[2].imshow(final_bg, alpha=0.55)
            if np.sum(skeleton) > 0:
                raw_graph = sknw.build_sknw(skeleton)
                # Apply A.3 Intelligent Pruning
                graph = prune_major_road_graph(raw_graph, RESOLUTION_M_PER_PX, final_bg.shape)
                
                # Plot the clean pruned graph
                # MultiGraph safe iteration
                for u, v in graph.edges():
                    edge_data = graph[u][v][0] if 0 in graph[u][v] else graph[u][v]
                    pts = edge_data['pts']
                    axes[2].plot(pts[:,1], pts[:,0], color='#ccff00', linewidth=3.5, alpha=1.0)
                    axes[2].scatter([pts[0,1]], [pts[0,0]], color='#ff0033', s=35, zorder=10)
                
                # Compute and store metrics
                height, width, _ = final_bg.shape
                tile_area_m2 = height * RESOLUTION_M_PER_PX * width * RESOLUTION_M_PER_PX
                m = compute_graph_quality_metrics(graph, RESOLUTION_M_PER_PX, tile_area_m2)
                m['tile_name'] = f
                all_metrics.append(m)
            else:
                import networkx as nx
                m = compute_graph_quality_metrics(nx.Graph(), RESOLUTION_M_PER_PX, 1000)
                m['tile_name'] = f
                all_metrics.append(m)
                
                # LEGACY: Old length-based naive pruning
                # for (s, e) in graph.edges():
                #     pts = graph.edges[s, e]['pts']
                #     if len(pts) > 35: # Pruning for total clarity
                #         # Neon Cyber-Yellow lines (#ccff00)
                #         axes[2].plot(pts[:,1], pts[:,0], color='#ccff00', linewidth=3.5, alpha=1.0)
                #         axes[2].scatter([pts[0,1]], [pts[0,0]], color='#ff0033', s=35, zorder=10)
            
            axes[2].set_title("Infrastructure Topology Graph", color='cyan', fontsize=20, pad=20)
            for ax in axes: ax.axis('off')
            
            plt.tight_layout()
            save_name = f.replace(".tif", "_GEOSIGHT_SIGNATURE.png")
            plt.savefig(os.path.join(OUTPUT_DIR, save_name), facecolor='#0a0a0a', dpi=250)
            plt.close()
            print(f"💎 Polished & Saved: {f} | Gate: {m['status']}")

        except Exception as e:
            print(f"❌ Error: {e}")

    # Generate the A.4 Output Metrics Report
    import csv
    METRICS_DIR = r"C:\Users\Mohvijay-sch\Desktop\GeoSight2\outputs\metrics"
    os.makedirs(METRICS_DIR, exist_ok=True)
    csv_path = os.path.join(METRICS_DIR, "tile_metrics.csv")
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['tile_name', 'connectivity', 'total_road_length_m', 'road_density_m_per_km2', 'dead_end_ratio', 'passed', 'status'])
        writer.writeheader()
        writer.writerows(all_metrics)
        
    passed_tiles = [m for m in all_metrics if m['passed']]
    failed_tiles = [m['tile_name'] for m in all_metrics if not m['passed']]
    avg_conn = sum(m['connectivity'] for m in all_metrics) / len(all_metrics) if all_metrics else 0
    avg_dens = sum(m['road_density_m_per_km2'] for m in all_metrics) / len(all_metrics) if all_metrics else 0
    
    print("\n" + "="*50)
    print(f"[GeoSight] Metrics Report: {len(passed_tiles)}/{len(all_metrics)} tiles PASSED | {len(failed_tiles)} FAILED")
    print(f"[GeoSight] Avg connectivity: {avg_conn:.2f} | Avg road density: {avg_dens:.1f} m/km²")
    if failed_tiles:
        print(f"[GeoSight] Failed tiles: {failed_tiles}")
    print("="*50)

if __name__ == "__main__":
    generate_signature_outputs()