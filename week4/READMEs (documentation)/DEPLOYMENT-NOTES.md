                                                            HestaBit Training Development
                                                                    Week 4 -Day 5

Project – Deployment Notes

## 1. Project Overview

The Week4 project is a **Product Management API** supporting:

- Create, retrieve, delete, restore, and notify products 
- Filtering, search, sorting, and pagination 
- Soft delete and restore functionality 
- Email notifications via job queue 
- Production-ready deployment using **PM2** in cluster mode 

**Conceptual Note:** PM2 ensures high availability, automatic restarts, and process monitoring. Cluster mode distributes requests across CPU cores for improved performance.

---

## 2. Folder Structure

```

week4/
├── src/
│   └── server.js           # Application entry point
├── prod/
│   └── ecosystem.config.js # PM2 production configuration
├── logs/                   # PM2 output logs
├── package.json
├── node_modules/
├── .env.prod               # Production environment variables
├── .env.example            # Template for environment variables
└── deployment-notes.md     # Deployment guide

```

---

## 3. Environment Variables

Create a `.env.prod` file in the project root:

```

PORT=3000
MONGO_URI=mongodb//localhost:3000/working_db
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
NODE_ENV=prod

```

Conceptual Note: Environment variables separate configuration from code. This ensures secure, flexible, and environment-specific setups.

---

## 4. PM2 Deployment

### 4.1 Install PM2 Globally

```
npm install -g pm2

```

**Conceptual Note:** PM2 manages Node.js processes, supports clustering, restarts on crashes, and centralizes logs.

---

### 4.2 Start the Application

```
pm2 start prod/ecosystem.config.js

```

* Loads `.env.prod` automatically via `env_file`
* Uses cluster mode for multiple CPU cores
* Auto-restarts crashed workers

![A Screenshot image of the start of apllication using pm2](screenshots/pm2_start.png)
---

### 4.3 Verify Application Status

```
pm2 status
```

* Confirms all workers are `online`
* Displays CPU and memory usage
* Shows restart counts for workers

![A screenshot image of pm2 status](screenshots/pm2_status.png)
---

### 4.4 View Logs

```
pm2 logs Week4
```

Or tail configured log files:

```
tail -f logs/Week4-out.log
tail -f logs/Week4-error.log
```

**Conceptual Note:** Cluster mode creates separate logs per worker. Merging logs simplifies monitoring and debugging.

![A screenshot image of pm2 logs](screenshots/pm2_logs.png)

#Logs are being written inside the src/logs/*.log files as well, so can check there as well

---

### 4.5 Restart / Stop / Delete

```
pm2 restart Week4
pm2 stop Week4
pm2 delete Week4
```

* **Restart:** reloads all workers without downtime
* **Stop:** stops all workers
* **Delete:** removes the app from PM2’s process list

---

## 5. Cluster Mode Notes

* Each CPU core runs a separate worker process
* Requests are distributed across workers to maximize throughput
* PM2 monitors and restarts crashed workers automatically
* Logs can be merged via `merge_logs: true` for simplified debugging

**Conceptual Note:** Node.js is single-threaded. Cluster mode allows multi-core utilization by spawning multiple processes.

---

## 6. Common Issues & Solutions

| Issue                         | Cause                                                             | Solution                                                          |
| ----------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| “No script path – aborting”   | PM2 config uses `app` instead of `apps`, or script path incorrect | Ensure `apps: [...]` and `script: '../src/server.js'`             |
| Application exits immediately | Missing environment variables or misconfigured paths              | Verify `.env.prod` exists and `env_file` path is correct          |
| No logs visible               | Cluster mode, logs not merged                                     | Enable `merge_logs: true` and configure `out_file` / `error_file` |
| App does not start on reboot  | PM2 process list not saved                                        | Run `pm2 save` and `pm2 startup`                                  |

---

## 7. Recommended Deployment Workflow

1. Pull latest code on server
2. Install production dependencies:

```
npm install --production
```

3. Ensure `.env.prod` exists and contains all required variables
4. Start or restart PM2:

```
pm2 start prod/ecosystem.config.js
```

5. Verify application status and monitor logs

6. Save PM2 process list to persist across reboots:

```
pm2 save
pm2 startup
```

---

## 8. Best Practices

* Keep `.env.prod` secure; never commit it to version control
* Monitor PM2 logs regularly for errors and warnings
* Merge cluster logs for simplified debugging
* Use cluster mode for high CPU utilization, fork mode for simpler single-instance deployments
* Test all environment variables locally before deploying to production

---

