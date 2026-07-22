FROM ubuntu:22.04
#noninteractive boot to prevent user input during installaion
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    curl \
    ca-certificates \
    gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
    && chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
&& rm -rf /var/lib/apt/lists/*

#dir set-up 
WORKDIR /git-bootstrap
#importing scipt
COPY git_env_setup.sh /git-bootstrap/
#executable
RUN chmod +x /git-bootstrap/git_env_setup.sh
#run on start up
ENTRYPOINT [ "/git-bootstrap/git_env_setup.sh" ]
