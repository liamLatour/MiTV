import 'package:flutter/material.dart';
import 'dart:math';
import '../classes/media_data.dart';

class PhotoViewer extends StatefulWidget {
  const PhotoViewer({Key? key, required this.data}) : super(key: key);

  final List<MediaData> data;

  @override
  State<PhotoViewer> createState() => _PhotoViewer();
}

class _PhotoViewer extends State<PhotoViewer> {

  // Responsive part
  double imgWidth = 100;
  double imgPadding = 5;

  List<Widget> getMediaFromURL(data) {
    List<Widget> media = <Widget>[];

    for (MediaData med in data) {
      if (med.type == "pic") {
        // https://docs.flutter.dev/cookbook/images/cached-images
        media.add(generateImage(med.url));
      } else if (med.type == "dir") {
        media.add(generateDir(med.url, med.thumbnail, med.eventName));
      } else if (med.type == "vid") {
        media.add(generateImage(med.url));
      }
    }

    return media;
  }

  Widget generateImage(url) {
    return Container(
      width: imgWidth,
      height: imgWidth / 1.5,
      padding: EdgeInsets.all(imgPadding),
      child: Image.network(
        "http://127.0.0.1:5000/media/" + url,
        fit: BoxFit.fitHeight,
        width: imgWidth,
        height: imgWidth / 1.5,
        cacheHeight: (imgWidth / 1.5 / 5).round(),
        cacheWidth: (imgWidth / 5).round(),
        loadingBuilder: (BuildContext context, Widget child,
            ImageChunkEvent? loadingProgress) {
          if (loadingProgress == null) return child;
          return Center(
            child: CircularProgressIndicator(
              value: loadingProgress.expectedTotalBytes != null
                  ? loadingProgress.cumulativeBytesLoaded /
                      loadingProgress.expectedTotalBytes!
                  : null,
            ),
          );
        },
      ),
    );
  }

  Widget generateVideo(url) {
    return Container(
      width: imgWidth,
      height: imgWidth / 1.5,
      padding: EdgeInsets.all(imgPadding),
      child: Image.network(
        "http://127.0.0.1:5000/media/" + url,
        fit: BoxFit.fitHeight,
        width: imgWidth,
        height: imgWidth / 1.5,
        cacheHeight: (imgWidth / 1.5 / 5).round(),
        cacheWidth: (imgWidth / 5).round(),
        loadingBuilder: (BuildContext context, Widget child,
            ImageChunkEvent? loadingProgress) {
          if (loadingProgress == null) return child;
          return Center(
            child: CircularProgressIndicator(
              value: loadingProgress.expectedTotalBytes != null
                  ? loadingProgress.cumulativeBytesLoaded /
                      loadingProgress.expectedTotalBytes!
                  : null,
            ),
          );
        },
      ),
    );
  }

  Widget generateDir(url, thumbnail, eventname) {
    return SizedBox(
      width: imgWidth,
      height: imgWidth / 1.5,
      child: GestureDetector(
        onTap: () {
          Navigator.pushNamed(context, url);
        },
        child: Container(
          margin: EdgeInsets.all(imgPadding),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(40),
            child: Stack(
              children: [
                SizedBox(
                  width: imgWidth,
                  height: imgWidth / 1.5,
                  child: Image.network(
                    "http://127.0.0.1:5000/media/" + thumbnail,
                    fit: BoxFit.cover,
                  ),
                ),
                Align(
                  alignment: Alignment.bottomCenter,
                  child: Container(
                    width: imgWidth,
                    height: imgWidth / 8,
                    decoration: const BoxDecoration(
                      color: Colors.black,
                    ),
                    alignment: Alignment.bottomCenter,
                    child: Text(
                      eventname,
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: imgWidth / 10,
                        backgroundColor: Colors.black,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    // Responsive part
    double screenWidth = MediaQuery.of(context).size.width;
    int factor = (screenWidth / 250).floor();
    imgWidth = screenWidth / min(factor, widget.data.length);
    imgPadding = 5;

    return Wrap(
      spacing: 0,
      runSpacing: 0,
      alignment: WrapAlignment.center,
      runAlignment: WrapAlignment.center,
      crossAxisAlignment: WrapCrossAlignment.center,
      children: getMediaFromURL(widget.data),
    );
  }
}
