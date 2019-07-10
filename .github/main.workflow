workflow "Test and upload on tag" {
  on = "push"
  resolves = ["Discord Webhook"]
}

action "Filter tag" {
  uses = "actions/bin/filter@master"
  args = "tag"
}

action "Twine upload" {
  uses = "orangutangaming/actions/twine-upload@master"
  secrets = ["TWINE_PASSWORD"]
  needs = ["Filter tag"]
  env = {
    TWINE_USERNAME = "OrangutanGaming"
  }
}

action "Uploads to Docker Hub" {
  uses = "orangutangaming/actions/docker-upload@master"
  needs = ["Twine upload"]
  env = {
    DOCKER_USERNAME = "orangutan"
    DOCKER_IMAGE_NAME = "owlw"
    DOCKER_NAMESPACE = "orangutan"
    DOCKER_IMAGE_TAG_SHA = "false"
  }
  secrets = ["DOCKER_PASSWORD"]
}

action "Discord Webhook" {
  uses = "Ilshidur/action-discord@master"
  needs = ["Uploads to Docker Hub"]
  secrets = ["DISCORD_WEBHOOK"]
  args = "Successfully deployed new PMA update."
}
