// TEST FILE - Security scanner validation only. DO NOT use in production.
// Purpose: Trigger Aikido Secrets scanner using AWS example credentials
// from AWS public documentation (not real credentials).

const config = {
  aws: {
    accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
    secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    region: 'us-east-1',
  },
};

module.exports = config;
