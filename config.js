// TEST FILE ONLY — Fake credentials for Aikido Secrets scanner validation.
// Values are from AWS public documentation examples. DO NOT USE IN PRODUCTION.

const config = {
  aws: {
    accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
    secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    region: 'us-east-1',
  },
  github: {
    token: 'ghp_16C7e42F292c6912E7710c838347Ae178B4a',
  },
  database: {
    password: 'Sup3rS3cr3tPassw0rd!',
    connectionString: 'postgresql://admin:Sup3rS3cr3tPassw0rd!@db.example.com:5432/prod',
  },
  stripe: {
    secretKey: 'sk_live_4eC39HqLyjWDarjtT1zdp7dc',
  },
};

module.exports = config;
