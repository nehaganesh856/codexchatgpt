export const getFileExtension = (filename) => {
  return filename.split('.').pop().toLowerCase();
};

export const getFileIcon = (filename) => {
  const ext = getFileExtension(filename);
  const iconMap = {
    js: '📄',
    jsx: '⚛️',
    ts: '📘',
    tsx: '⚛️',
    css: '🎨',
    html: '📝',
    json: '{}',
    py: '🐍',
    sql: '🗄️',
  };
  return iconMap[ext] || '📋';
};

export const downloadFile = (blob, filename) => {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

export const readFileAsText = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => resolve(e.target.result);
    reader.onerror = reject;
    reader.readAsText(file);
  });
};

export const validateFileType = (file, allowedTypes) => {
  return allowedTypes.includes(file.type);
};

export const validateFileSize = (file, maxSizeMB) => {
  return file.size <= maxSizeMB * 1024 * 1024;
};