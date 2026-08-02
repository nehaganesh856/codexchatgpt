
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import DashboardLayout from '../components/layout/DashboardLayout';
import ProjectList from '../components/projects/ProjectList';
import CreateProject from '../components/projects/CreateProject';
import { Plus, Loader } from 'lucide-react';
import toast from 'react-hot-toast';
import { projectService } from '../services/projectService';

function Dashboard() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [projects, setProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await projectService.getProjects();
      setProjects(data || []);
    } catch (err) {
      let errorMessage = "Failed to load projects";

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

  const handleProjectCreated = (newProject) => {
    setProjects((prev) => [newProject, ...prev]);
    setShowCreateModal(false);
    toast.success('Project created successfully!');
  };

  const handleProjectDeleted = (projectId) => {
    setProjects((prev) => prev.filter((p) => p.id !== projectId));
    toast.success('Project deleted');
  };

  const handleProjectClick = (projectId) => {
    navigate(`/projects/${projectId}`);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-white">Projects</h1>
            <p className="text-slate-400 mt-1">
              Welcome back, {user?.name || 'User'}! Manage your AI-generated applications.
            </p>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn btn-primary"
          >
            <Plus className="w-4 h-4" />
            New Project
          </button>
        </div>

        {/* Error State */}
        {error && (
          <div className="p-4 bg-red-900/20 border border-red-800 rounded-lg text-red-400">
            {error}
            <button
              onClick={loadProjects}
              className="ml-4 text-red-300 hover:text-red-200 underline"
            >
              Try again
            </button>
          </div>
        )}

        {/* Loading State */}
        {isLoading ? (
          <div className="flex justify-center items-center py-20">
            <div className="flex flex-col items-center gap-3">
              <Loader className="w-8 h-8 animate-spin text-blue-500" />
              <p className="text-slate-400">Loading projects...</p>
            </div>
          </div>
        ) : projects.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-slate-400 mb-6">
              <p className="text-lg mb-2">No projects yet</p>
              <p className="text-sm">
                Create your first project to get started with AI-powered app generation.
              </p>
            </div>
            <button
              onClick={() => setShowCreateModal(true)}
              className="btn btn-primary"
            >
              <Plus className="w-4 h-4" />
              Create First Project
            </button>
          </div>
        ) : (
          <ProjectList
            projects={projects}
            onProjectClick={handleProjectClick}
            onProjectDeleted={handleProjectDeleted}
          />
        )}
      </div>

      {/* Create Project Modal */}
      {showCreateModal && (
        <CreateProject
          onClose={() => setShowCreateModal(false)}
          onSuccess={handleProjectCreated}
        />
      )}
    </DashboardLayout>
  );
}

export default Dashboard;
