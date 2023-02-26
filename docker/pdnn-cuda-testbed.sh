XSOCK=/tmp/.X11-unix
XAUTH=$HOME/.Xauthority
#XIMAGE=/media/mobilitylab/6717202b-0641-47a2-87de-0a71081a18241

VOLUMES="--volume=$XSOCK:$XSOCK:rw
         --volume=$XAUTH:$XAUTH:rw
	 --volume=$XIMAGE:/home/mobilitylab/dataset:rw"

IMAGE=liangkailiu/pdnn-testbed:v0.3

echo "Launching $IMAGE"

sudo docker run \
    -it \
    --gpus all \
    $VOLUMES \
    --env="XAUTHORITY=${XAUTH}" \
    --env="DISPLAY=${DISPLAY}" \
    --privileged \
    --net=host \
    $RUNTIME \
    $IMAGE \
    /bin/bash
