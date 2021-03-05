declare var require: any;

export const environment = {
  production: false,
  name: require('../../package.json').name,
  // applicationId: require('../../package.json').id,
  version: require('../../package.json').version,
};
