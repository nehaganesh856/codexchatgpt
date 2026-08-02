import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/layout/DashboardLayout';
import { Loader, ArrowLeft, Save } from 'lucide-react';
import toast from 'react-hot-toast';
import { projectService } from '../services/projectService';

function ProjectSettings() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });

  useEffect(() => {
    loadProject();
  }, [id]);

  const loadProject = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await projectService.getProject(id);
      setProject(data);
      setFormData({
        name: data.name,
        description: data.description,
      });
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

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSave = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    try {
      await projectService.updateProject(id, formData);
      toast.success('Project updated successfully');
      loadProject();
    } catch (err) {
      let errorMessage = "Failed to update project";

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
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex justify-center items-center py-20">
          <div className="flex flex-col items-center gap-3">
            <Loader className="w-8 h-8 animate-spin text-blue-500" />
            <p className="text-slate-400">Loading project settings...</p>
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
      <div className="max-w-2xl">
        <button
          onClick={() => navigate(`/projects/${id}`)}
          className="flex items-center gap-2 text-slate-300 hover:text-white transition mb-8"
        >
          <ArrowLeft className="w-4 h-4" />
          Back
        </button>

        <div className="card">
          <h1 className="text-3xl font-bold text-white mb-8">Project Settings</h1>

          <form onSubmit={handleSave} className="space-y-6">
            {/* Project Name */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-slate-200 mb-2">
                Project Name
              </label>
              <input
                id="name"
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Project name"
                disabled={isSaving}
                className="w-full"
              />
            </div>

            {/* Description */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-slate-200 mb-2">
                Description
              </label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Project description"
                disabled={isSaving}
                rows={6}
                className="w-full resize-none"
              />
            </div>

            {/* Submit Button */}
            <div className="flex gap-3">
              <button
                type="submit"
                disabled={isSaving}
                className="btn btn-primary"
              >
                <Save className="w-4 h-4" />
                {isSaving ? 'Saving...' : 'Save Changes'}
              </button>
              <button
                type="button"
                onClick={() => navigate(`/projects/${id}`)}
                disabled={isSaving}
                className="btn btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default ProjectSettings;
