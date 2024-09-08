// src/logger.js
import log from 'loglevel';

console.log('Environment Variables:', import.meta.env); // Log to verify

const logLevel = import.meta.env.VITE_APP_LOG_LEVEL || (import.meta.env.MODE === 'production' ? 'warn' : 'debug');
log.setLevel(logLevel);

export default log;
