import { X } from 'lucide-react';

function Modal({ isOpen, onClose, title, children, size = 'md' }) {
  if (!isOpen) return null;

  const sizeClass = {
    sm: 'w-full max-w-sm',
    md: 'w-full max-w-md',
    lg: 'w-full max-w-lg',
    xl: 'w-full max-w-xl',
  }[size];

  return (
    <div className="modal-backdrop">
      <div className={`bg-slate-800 border border-slate-700 rounded-lg p-8 ${sizeClass} animate-slideInUp`}>
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          {title && <h2 className="text-2xl font-bold text-white">{title}</h2>}
          <button
            onClick={onClose}
            className="p-1 hover:bg-slate-700 rounded-lg transition"
          >
            <X className="w-5 h-5 text-slate-400" />
          </button>
        </div>

        {/* Content */}
        {children}
      </div>
    </div>
  );
}

export default Modal;