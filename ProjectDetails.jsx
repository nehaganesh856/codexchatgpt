import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/layout/DashboardLayout';
import { Loader, ArrowLeft, Settings, Edit, Trash2 } from 'lucide-react';
import toast from 'react-hot-toast';
import { projectService } from '../services/projectService';
import { formatDistanceToNow } from 'date-fns';

function ProjectDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    loadProject();
  }, [id]);

  const loadProject = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await projectService.getProject(id);
      setProject(data);
    } catch (err) {
      let errorMessage = "Failed to load project";

      const detail = err?.response?.data?.detail;

      if (typeof detail === "string") {
        errorMessage = detail;
      } else if (Array.isArray(detail)) {
        errorMessage = detail
          .map((item) => item.msg || JSON.stringify(item))
          .join(", ");
      } else if (detail && typeof detail === "object") {
        errorMessage = detail.msg || JSON.stringify(detail);
      } else if (err?.message) {
        errorMessage = err.message;
      }

      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (
      !window.confirm(
        'Are you sure you want to delete this project? This action cannot be undone.'
      )
    ) {
      return;
    }

    setIsDeleting(true);
    try {
      await projectService.deleteProject(id);
      toast.success('Project deleted successfully');
      navigate('/dashboard');
    } catch (err) {
      let errorMessage = "Failed to delete project";

      const detail = err?.response?.data?.detail;

      if (typeof detail === "string") {
        errorMessage = detail;
      } else if (Array.isArray(detail)) {
        errorMessage = detail
          .map((item) => item.msg || JSON.stringify(item))
          .join(", ");
      } else if (detail && typeof detail === "object") {
        errorMessage = detail.msg || JSON.stringify(detail);
      } else if (err?.message) {
        errorMessage = err.message;
      }

      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setIsDeleting(false);
    }
  };

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex justify-center items-center py-20">
          <div className="flex flex-col items-center gap-3">
            <Loader className="w-8 h-8 animate-spin text-blue-500" />
            <p className="text-slate-400">Loading project...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (error || !project) {
    return (
      <DashboardLayout>
        <div className="text-center py-20">
          <p className="text-red-400 mb-4">{error || 'Project not found'}</p>
          <button
            onClick={() => navigate('/dashboard')}
            className="btn btn-primary"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Dashboard
          </button>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2 text-slate-300 hover:text-white transition"
          >
            <ArrowLeft className="w-4 h-4" />
            Back
          </button>
          <div className="flex gap-2">
            <button
              onClick={() => navigate(`/projects/${id}/editor`)}
              className="btn btn-primary"
            >
              <Edit className="w-4 h-4" />
              Edit Project
            </button>
            <button
              onClick={() => navigate(`/projects/${id}/settings`)}
              className="btn btn-secondary"
            >
              <Settings className="w-4 h-4" />
              Settings
            </button>
            <button
              onClick={handleDelete}
              disabled={isDeleting}
              className="btn bg-red-600 text-white hover:bg-red-700 disabled:opacity-50"
            >
              <Trash2 className="w-4 h-4" />
              {isDeleting ? 'Deleting...' : 'Delete'}
            </button>
          </div>
        </div>

        {/* Project Info */}
        <div className="card">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-white mb-2">{project.name}</h1>
            <p className="text-slate-300">{project.description}</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-slate-700 rounded-lg p-4">
              <p className="text-xs text-slate-400 mb-1">Status</p>
              <p className="text-sm font-semibold text-white capitalize">
                {project.status || 'Draft'}
              </p>
            </div>
            <div className="bg-slate-700 rounded-lg p-4">
              <p className="text-xs text-slate-400 mb-1">Created</p>
              <p className="text-sm font-semibold text-white">
                {formatDistanceToNow(new Date(project.created_at), {
                  addSuffix: true,
                })}
              </p>
            </div>
            <div className="bg-slate-700 rounded-lg p-4">
              <p className="text-xs text-slate-400 mb-1">Updated</p>
              <p className="text-sm font-semibold text-white">
                {formatDistanceToNow(new Date(project.updated_at), {
                  addSuffix: true,
                })}
              </p>
            </div>
            <div className="bg-slate-700 rounded-lg p-4">
              <p className="text-xs text-slate-400 mb-1">ID</p>
              <p className="text-sm font-mono text-blue-400 truncate">{project.id}</p>
            </div>
          </div>
        </div>

        {/* Files */}
        {project.files && project.files.length > 0 && (
          <div className="card">
            <h2 className="text-xl font-semibold text-white mb-4">Files</h2>
            <div className="space-y-2">
              {project.files.map((file) => (
                <div
                  key={file.id}
                  className="p-3 bg-slate-700 rounded-lg flex items-center justify-between hover:bg-slate-600 transition"
                >
                  <span className="text-slate-300">{file.name}</span>
                  <span className="text-xs text-slate-400">{file.type}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Project Statistics */}
        {project.statistics && (
          <div className="card">
            <h2 className="text-xl font-semibold text-white mb-4">Statistics</h2>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="p-4 bg-blue-900/20 border border-blue-700 rounded-lg">
                <p className="text-sm text-slate-400 mb-1">Total Files</p>
                <p className="text-2xl font-bold text-blue-400">
                  {project.statistics.files || 0}
                </p>
              </div>
              <div className="p-4 bg-green-900/20 border border-green-700 rounded-lg">
                <p className="text-sm text-slate-400 mb-1">Lines of Code</p>
                <p className="text-2xl font-bold text-green-400">
                  {project.statistics.lines_of_code || 0}
                </p>
              </div>
              <div className="p-4 bg-purple-900/20 border border-purple-700 rounded-lg">
                <p className="text-sm text-slate-400 mb-1">Components</p>
                <p className="text-2xl font-bold text-purple-400">
                  {project.statistics.components || 0}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default ProjectDetails;
