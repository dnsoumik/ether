declare var require: any;

export const environment = {
  production: true,
  name: require('../../package.json').name,
  // applicationId: require('../../package.json').id,
  version: require('../../package.json').version,
};
