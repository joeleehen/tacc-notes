# Docker Containers
>[!warning] CMD vs ENTRYPOINT
> We had a Dockerfile that built a python app from a poetry wheel build. We dumped the build tools and put the app in a new image.
> Our desired behavior is to display help messages when the container is run without arguments. If an argument is passed, you use that argument as the number of iterations for our Monte-Carlo simulation.
> This was achieved with a `CMD` layer at the end of our Dockerfile
> ```dockerfile
> CMD ["calculate-pi", "--help"]
> ```
> This implementation displays the desired default help message, but passing an argument throws an error:
> ![[Screenshot 2024-09-20 at 11.41.12 AM.png]]
> We resolve this behavior by instead setting an `ENTRYPOINT` to our Python tool. Our `CMD` layer still displays the help message when the container is ran without arguments, but is overridden when an argument passed.
> ```dockerfile
> ENTRYPOINT [calculate-pi]
> CMD [ calculate-pi, --help ]
> ```
> The `CMD` is overridden when an argument is passed. Instead of passing the argument to Docker (which thinks the argument is a container process and freaks out), the argument is passed to our Python `ENTRYPOINT`

Before you start using docker in the command line, you *must* first start the Docker application. This starts the docker daemon, which is required to use the docker CLI.

>[!check] Docker CLI
Build an image like this:
`docker build -t joeleehen/containerName:verNum .`
#note Use the `-f` flag to pass a specific Dockerfile
>
Running a container is simple
`docker run --rm -it joeleehen/containerName:verNum`
#note the `-it` flag runs the container interactively, sometimes omitted
## Multi-stage Builds
Sometimes containers can be pretty big. Using multi-stage builds can alleviate container sizes.
Each `FROM` statement in a Dockerfile is another stage of the build. For example:
``` dockerfile
FROM golang:1.21
WORKDIR /src

COPY app.go .

RUN CGO_ENABLED=0 go build -o /usr/loca/bin/hello ./app.go

CMD ["/usr/local/bin/hello"]
```
has a single stage. We base our image off the official Go image and copy/compile some Go app we wrote. This results in an image of 834Mb, pretty big for what the image does!

We can use multiple stages to make the image smaller.
``` dockerfile
FROM golang:1.21 AS build
WORKDIR /src

COPY app.go .

RUN CGO_ENABLED=0 go build -o /usr/local/bin/hello ./app.go

FROM alpine:3.18.3

COPY --from=build /usr/local/bin/hello /usr/local/bin/hello

CMD ["/usr/local/bin/hello"]
```
*Two* stages! Our first stage grabs the image with all the Go tools we need and compiles our Go app. From there, we copy the compiled app to a lightweight Alpine image and get rid of all the Go tools. This way we can compile with the Go stuff we need and get rid of it when we're done! The resulting build is **9.26MB**.

---
# Multi-Architecture Builds
#### Targeting a single platform
We can usually specify a single target through our build command:
`docker build --platform linux/amd64 -t joeleehen/blahblahblah:0.0.1 .`
You can check if the build targeted the correct platform by `docker inspect`ing the image or by passing `uname -m` to the container.
## Multiple Platform Targets
We need to use a different build tool, `docker buildx`.
>[!example] From the example docs
> We built our own builder using the docker-container builder
> ```bash
> docker buildx create --name mybuilder --bootstrap --use
> ```
> and then build an example image
> ```bash
> docker buildx build --platform linux/arm64 linux/amd64 -t joeleehen/curl-example:0.0.1 .
> ```

You **cannot** have multiple images of the same name with different architectures! Nothing is loaded into the docker daemon; te new builds are kept in the *build cache*. To create the manifest and push them to Docker Hub, use
```bash
docker buildx build --platform linux/arm64,linux/amd64 -t joeleehen/curl-example:0.1.1 --push .
```
