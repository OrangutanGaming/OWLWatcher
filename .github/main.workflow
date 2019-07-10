workflow "Test and upload on tag" {
  on = "push"
  resolves = ["Discord Webhook"]
}

action "Filter tag" {
  uses = "actions/bin/filter@master"
  args = "tag"
}

action "Test 3.5" {
  uses = "orangutangaming/actions/pytest-install-35@master"
  needs = ["Filter tag"]
}

action "Test 3.6" {
  uses = "orangutangaming/actions/pytest-install-36@master"
  needs = ["Filter tag"]
}

action "Test 3.7" {
  uses = "orangutangaming/actions/pytest-install-37@master"
  needs = ["Filter tag"]
}

action "Twine upload" {
  uses = "orangutangaming/actions/twine-upload@master"
  secrets = ["TWINE_USERNAME", "TWINE_PASSWORD"]
  needs = ["Test 3.5", "Test 3.6", "Test 3.7"]
}

action "Uploads to Docker Hub" {
  uses = "orangutangaming/actions/docker-upload@master"
  needs = ["Twine upload"]
  env = {
    DOCKER_USERNAME = "orangutan"
    DOCKER_IMAGE_NAME = "pma"
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
