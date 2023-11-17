db.createUser({
  user: 'root',
  pwd: 'example',
  roles: [
    { role: 'clusterMonitor', db: 'admin' },
    { role: 'dbOwner', db: 'db_name' },
    { role: 'readWrite', db: 'db_crashell' },
  ],
});
