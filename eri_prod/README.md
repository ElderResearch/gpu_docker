# eri production gpu docker image

at the current time, this is *identical* to the `eri_dev` docker image in the neighboring directory (the difference between prod and dev is simply the way the image is run and the container is constructed). until an actual difference exists between these images, let's not create a new `Dockerfile`, and instead just be conscious about creating a new tag name from the `eri_dev/Dockerfile`
