export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    LOGOUT: '/auth/logout',
    ME: '/auth/me',
  },
  PROJECTS: {
    LIST: '/projects',
    CREATE: '/projects',
    GET: (id) => `/projects/${id}`,
    UPDATE: (id) => `/projects/${id}`,
    DELETE: (id) => `/projects/${id}`,
    GENERATE: '/projects/generate',
  },
};

export const PROJECT_STATUS = {
  DRAFT: 'draft',
  GENERATING: 'generating',
  GENERATED: 'generated',
  FAILED: 'failed',
  DEPLOYING: 'deploying',
  DEPLOYED: 'deployed',
};

export const NOTIFICATION_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  INFO: 'info',
  WARNING: 'warning',
};

export const DEVICE_SIZES = {
  MOBILE: { width: 375, height: 812 },
  TABLET: { width: 768, height: 1024 },
  DESKTOP: { width: 1920, height: 1080 },
};