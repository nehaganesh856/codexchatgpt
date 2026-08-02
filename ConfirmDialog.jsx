import { AlertCircle } from 'lucide-react';

function ConfirmDialog({
  isOpen,
  title,
  message,
  onConfirm,
  onCancel,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  isDangerous = false,
}) {
  if (!isOpen) return null;

  return (
    <div className="modal-backdrop">
      <div className="bg-slate-800 border border-slate-700 rounded-lg p-8 w-full max-w-md animate-slideInUp">
        <div className="flex items-center gap-3 mb-4">
          {isDangerous && (
            <AlertCircle className="w-6 h-6 text-red-500 flex-shrink-0" />
          )}
          <h2 className="text-xl font-bold text-white">{title}</h2>
        </div>

        <p className="text-slate-300 mb-6">{message}</p>

        <div className="flex gap-3">
          <button
            onClick={onCancel}
            className="btn btn-secondary flex-1"
          >
            {cancelText}
          </button>
          <button
            onClick={onConfirm}
            className={`btn flex-1 ${
              isDangerous
                ? 'bg-red-600 text-white hover:bg-red-700'
                : 'btn-primary'
            }`}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmDialog;