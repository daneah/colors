# colors

This is a tiny script that performs k-means clustering on the colors in an image to display the most prominent overall colors.

## Usage

```shell
$ python colors.py <image file path> <number of colors to extract> <display height of image in pixels>
```

The script will output HTML that you can view in your browser. As an example, running the following command:

```shell
$ python colors.py pittsburgh.jpg 6 300 > index.html
```

will product an HTML page viewable in your browser that looks like the following screenshot:

![Screenshot of output HTML](screenshot.png)
