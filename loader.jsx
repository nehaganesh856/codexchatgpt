export function Spinner({ size = 'md', className }) {
  const sizeClass = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  }[size];

  return (
    <div className={`${sizeClass} ${className}`}>
      <div className="spinner" />
    </div>
  );
}

export function SkeletonLoader({ lines = 3 }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: lines }).map((_, i) => (
        <div key={i} className="h-4 bg-slate-700 rounded animate-pulse" />
      ))}
    </div>
  );
}