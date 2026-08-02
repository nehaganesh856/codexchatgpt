import { useState } from 'react';
import { X, Save, Loader } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { projectService } from '../../services/projectService';

function EditorLayout({ project, onProjectUpdate }) {
  const navigate = useNavigate();
  const [code, setCode] = useState(project?.code || '');
  const [isSaving, setIsSaving] = useState(false);

  const handleSave = async () => {
    setIsSaving(true);
    try {
      const updated = await projectService.updateProject(project.id, {
        code,
      });
      onProjectUpdate(response.project);
      toast.success('Code saved successfully!');
    } catch (err) {
      toast.error('Failed to save code');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex flex-col">
      {/* Header */}
      <div className="bg-slate-800 border-b border-slate-700 px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-white">{project.name}</h1>
        <div className="flex gap-2">
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="btn btn-primary"
          >
            {isSaving ? (
              <>
                <Loader className="w-4 h-4 animate-spin" />
                Saving...
              </>
            ) : (
              <>
                <Save className="w-4 h-4" />
                Save
              </>
            )}
          </button>
          <button
            onClick={() => navigate(`/projects/${project.id}`)}
            className="btn btn-ghost"
          >
            <X className="w-4 h-4" />
            Close
          </button>
        </div>
      </div>

      {/* Editor */}
      <div className="flex-1 flex">
        <div className="flex-1 overflow-hidden">
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="w-full h-full p-4 bg-slate-900 text-slate-100 font-mono text-sm border-none resize-none focus:outline-none focus:ring-0"
            placeholder="Your code here..."
          />
        </div>
      </div>
    </div>
  );
}

export default EditorLayout;