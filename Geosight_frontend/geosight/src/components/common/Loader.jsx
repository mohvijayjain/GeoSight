import './Loader.css';

function Loader({ message = 'Processing...' }) {
  return (
    <div className="loader">
      <div className="spinner"></div>
      <p>{message}</p>
    </div>
  );
}

export default Loader;
