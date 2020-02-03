# SSR Client in Docker

[![](https://github.com/gwy15/ssr-client-docker/workflows/Build%20docker/badge.svg)](https://github.com/gwy15/ssr-client-docker/actions)

## Configuration

The ssr client loads config.json from `/config/config.json`, so mount your config directory to this path. And that should do it.

## Usage

### Run in front ground (for debug or use supervisord)

```bash
sudo docker run -it --rm --name=ssr-client -p 1080:1080 -v $(pwd)/config:/config ssr-client-docker
```

### Run in background (for docker images)
```bash
sudo docker run -d --rm --name=ssr-client -p 1080:1080 -v $(pws)/config:/config ssr-client-docker
```
