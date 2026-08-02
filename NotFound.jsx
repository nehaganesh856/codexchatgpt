import { useNavigate } from 'react-router-dom';
import { AlertCircle, Home } from 'lucide-react';

function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
      <div className="text-center">
        <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-6" />
        <h1 className="text-5xl font-bold text-white mb-2">404</h1>
        <p className="text-xl text-slate-300 mb-8">Page not found</p>
        <p className="text-slate-400 mb-8 max-w-md">
          The page you're looking for doesn't exist. It might have been moved or deleted.
        </p>
        <button
          onClick={() => navigate('/')}
          className="btn btn-primary"
        >
          <Home className="w-4 h-4" />
          Go Home
        </button>
      </div>
    </div>
  );
}

export default NotFound;