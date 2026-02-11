# Week 5 — Day 1

### Docker Fundamentals & Linux Exploration Inside Containers

---

## Objective

Day 1 focused on:

* Understanding Docker images and containers
* Writing a production-style Dockerfile
* Running a Node.js container
* Entering the container shell
* Exploring Linux environment inside a running container
* Observing processes, filesystem, disk usage, and logs

This session emphasized **practical container inspection**.

---

## Dockerfile – Node Application

```
FROM node:20-alpine

WORKDIR /week5-app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "index.js"]
```

### Why This Structure?

* `node:20-alpine` → Lightweight production-ready base image
* `WORKDIR` → Clean application structure
* `npm ci --omit=dev` → Deterministic, production install
* `EXPOSE` → Documents container port

---

### Build Docker Image

```
docker build -t week5-day1-node .
```

![Docker Build Output](../Screenshots/day1/day1_docker_build.png)

---

### Run Container

```
docker run -d -p 3000:3000 --name week5-day1 week5-day1-node
```

![Docker Run Output](../Screenshots/day1/docker_run.png)

---

### Verify Running Container

```
docker ps
```

Purpose:

* Confirm container status
* Check port mapping
* Verify container name

![Docker PS Output](../Screenshots/day1/docker_ps.png)

---

## Enter Container Shell (Like SSH)

```
docker exec -it week5-day1 /bin/sh
```

This provides direct shell access inside the container.

![Docker Exec Shell](../Screenshots/day1/Main_Query.png)

---

## Explore Filesystem Inside Container

### List Files

```
ls
```

Observation:

* Alpine-based minimal Linux environment
* Standard Linux directory structure


![LS Output](../Screenshots/day1/shell/Query_ls.png)


## Inspect Running Processes

### Show Running Processes

```
ps
```

Observation:

* Node runs as PID 1
* Container lifecycle tied to main process

![PS Output](../Screenshots/day1/shell/Query_ps.png)

---

### Monitor System Resources

```
top
```

Purpose:

* Observe CPU and memory usage
* Identify active processes

![TOP Output](../Screenshots/day1/shell/Query_top.png)

---

## Inspect Disk Usage

### Filesystem Usage

```
df -h
```

![DF Output](../Screenshots/day1/shell/Query_df.png)

---

## View Container Logs (Outside Container)

Exit shell:

```
exit
```

![Exit Shell](../Screenshots/day1/shell/Query_exit.png)

---

View logs:

```
docker logs week5-day1
```

Purpose:

* Inspect runtime output
* Debug application behavior

![Docker Logs](../Screenshots/day1/day1_log.png)
