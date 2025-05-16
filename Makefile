# Zawsze budujls 
.PHONY: build
# Zmienne
NAME_APP=appmqtt
DOCKER_REGISTRY=192.168.8.129:8101
IMAGE_NAME = $(DOCKER_REGISTRY)/$(NAME_APP)
TAG = $(shell date +'%Y%m%d%H%M%S')  # Generuje tag oparty na dacie
FULL_IMAGE_NAME = $(IMAGE_NAME):$(TAG)

# Reguła budowania obrazu Docker
build:
	docker build -t $(NAME_APP) .
	docker tag  $(NAME_APP) $(IMAGE_NAME)

# Reguła wysyłania obrazu na Docker Hub
push: build
	docker push $(IMAGE_NAME)

save: build
	docker save $(NAME_APP) > $(NAME_APP).tar

# Reguła uruchamiająca budowanie i wysyłanie
all: build push