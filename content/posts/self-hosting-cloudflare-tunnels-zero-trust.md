Title: Self-hosting through Cloudflare Tunnels: zero-trust without the enterprise overhead
Date: 2026-03-10
Category: Infra
Slug: self-hosting-cloudflare-tunnels-zero-trust
Summary: Expose home lab services and personal applications securely without opening inbound ports or setting up dynamic DNS, using Cloudflare's egress-only secure tunnels.

Self-hosting personal projects on local hardware (like a home **Proxmox VE cluster** or Intel NUC) usually comes with networking headaches: managing dynamic public IPs, configuring NAT port-forwarding, or purchasing static IPs. Furthermore, opening inbound ports (like `80` and `443`) on a home router exposes your home network directly to global automated scanning and brute-force campaigns.

**Cloudflare Tunnels** (`cloudflared`) resolve this by introducing an outbound-only connection pattern. Instead of opening ports to the world, a lightweight daemon runs in your local network and establishes secure, persistent outbound connections to the nearest Cloudflare edge servers.

```
+------------------+                   +--------------------+                   +-------------------+
|  Local Service   |   == Outbound =>  |  cloudflared side  |   == Outbound =>  |  Cloudflare Edge  |
|  (Nginx / App)   |                   |  (Docker Container)|                   |  (Public Gateway) |
+------------------+                   +--------------------+                   +-------------------+
```

## How It Works: Egress-Only Topology

Because the daemon creates an *outbound* connection (egress), your home firewall or carrier-grade NAT (CGNAT) naturally allows it, without needing any port forwards. When a recruiter navigates to `https://subba.dev`, Cloudflare's edge proxy receives the traffic, handles the TLS/SSL handshake, applies security policies, and routes the requests down the established tunnel directly to the local daemon, which forwards it to the web server on the internal Docker network.

## The Local Configuration (`config.yml`)

The daemon is configured using a simple declarative YAML file. Here is the configuration file running in production for `subba.dev`:

```yaml
# cloudflared.config.yml
tunnel: 4c9e4210-91c2-4876-b6d3-cb3fb0c49021
credentials-file: /etc/cloudflared/tunnel-credentials.json

ingress:
  # Route subba.dev to the internal Nginx web server
  - hostname: subba.dev
    service: http://nginx-web:80
  
  # Route www.subba.dev to the same Nginx container
  - hostname: www.subba.dev
    service: http://nginx-web:80

  # Catch-all: Respond with 404 for unconfigured hostnames
  - service: http_status:404
```

## Docker-Compose Architecture

To guarantee high availability and isolation, we package the tunnel daemon alongside the web server inside a Docker Compose network. The Nginx server is completely hidden from the host machine (no ports are published to the host OS):

```yaml
version: '3.8'

services:
  nginx-web:
    image: nginx:alpine
    container_name: nginx-web
    restart: unless-stopped
    volumes:
      - ./output:/usr/share/nginx/html:ro
    # Note: No 'ports' section! Completely isolated from the host network.

  tunnel:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared-tunnel
    restart: unless-stopped
    command: tunnel --config /etc/cloudflared/config.yml run
    volumes:
      - ./cloudflared.config.yml:/etc/cloudflared/config.yml:ro
      - ./credentials.json:/etc/cloudflared/tunnel-credentials.json:ro
    depends_on:
      - nginx-web
```

## Security Controls

Running this egress-only model yields immediate security advantages:
1. **DDoS Protection**: Traffic is absorbed and filtered at Cloudflare's edge network before reaching your home lab.
2. **IP Masking**: Your residential public IP address is never revealed in DNS lookups.
3. **Identity-Aware Access**: Through Cloudflare Zero Trust, you can enforce access policies (e.g., Google OAuth or single-use pin validation) directly at the edge, protecting private directories from unauthorized external users.

This boring, reliable infrastructure choice provides a secure and highly scalable deployment footprint, ideal for hosting recruiter-facing resources without enterprise maintenance overhead.
