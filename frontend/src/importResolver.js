/**
 * Custom import resolver for path aliases
 * Used in conjunction with babel-plugin-module-resolver
 */
const path = require('path');

module.exports = function resolveImport(sourcePath) {
  if (sourcePath.startsWith('@/')) {
    return sourcePath.replace('@/', path.resolve(__dirname) + '/');
  }
  
  if (sourcePath.startsWith('@components/')) {
    return sourcePath.replace('@components/', path.resolve(__dirname, 'components') + '/');
  }
  
  if (sourcePath.startsWith('@hooks/')) {
    return sourcePath.replace('@hooks/', path.resolve(__dirname, 'hooks') + '/');
  }
  
  if (sourcePath.startsWith('@types/')) {
    return sourcePath.replace('@types/', path.resolve(__dirname, 'types') + '/');
  }
  
  if (sourcePath.startsWith('@context/')) {
    return sourcePath.replace('@context/', path.resolve(__dirname, 'context') + '/');
  }
  
  if (sourcePath.startsWith('@utils/')) {
    return sourcePath.replace('@utils/', path.resolve(__dirname, 'utils') + '/');
  }
  
  return sourcePath;
};
