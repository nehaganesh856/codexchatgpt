import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/layout/DashboardLayout';
import EditorLayout from '../components/layout/EditorLayout';
import { Loader, ArrowLeft } from 'lucide-react';
import toast from 'react-hot-toast';
import { projectService } from '../services/projectService';

function ProjectEditor() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadProject();
  }, [id]);
  console.log("ProjectEditor loaded");

  const loadProject = async () => {
    console.log("Project ID:", id);
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

  if (isLoading) {
    return (
      <DashboardLayout>
        <div className="flex justify-center items-center py-20">
          <div className="flex flex-col items-center gap-3">
            <Loader className="w-8 h-8 animate-spin text-blue-500" />
            <p className="text-slate-400">Loading project editor...</p>
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
    <EditorLayout project={project} onProjectUpdate={setProject} />
  );
}

export default ProjectEditor;
