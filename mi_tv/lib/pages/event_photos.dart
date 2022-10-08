import 'package:flutter/material.dart';
import 'package:video_js/video_js.dart';
import 'package:http/http.dart' as http;
import 'dart:async';
import 'dart:convert';
import '../widgets/photo_viewer.dart';
import '../classes/media_data.dart';


/// This file is used to display pictures and videos in a given folder
///

// https://pub.dev/packages/flutter_staggered_grid_view
// https://flutterawesome.com/flutter-plugin-for-use-video-js-in-flutter-web/
// https://blurha.sh/
// https://docs.flutter.dev/cookbook/images/fading-in-images
class PhotosPage extends StatefulWidget {
  const PhotosPage({Key? key, this.url = ""}) : super(key: key);

  final String url;

  @override
  State<PhotosPage> createState() => _PhotosPageState();
}

class _PhotosPageState extends State<PhotosPage> {
  late Future<Media> futureMedia;

  @override
  void initState() {
    super.initState();
    futureMedia = fetchMedia();
  }

  Future<Media> fetchMedia() async {
    final response = await http.get(
        Uri.parse('http://127.0.0.1:5000/media/' + widget.url),
        headers: {'Content-Type': 'application/json; charset=utf-8'});

    if (response.statusCode == 200) {
      return Media.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load media');
    }
  }

  VideoJsController videoWidget(String url) {
    return VideoJsController(
      "videoId",
      videoJsOptions: VideoJsOptions(
          controls: true,
          loop: false,
          muted: false,
          // poster: 'https://file-examples-com.github.io/uploads/2017/10/file_example_JPG_100kB.jpg',
          aspectRatio: '16:9',
          fluid: false,
          language: 'en',
          liveui: false,
          notSupportedMessage: 'this movie type not supported',
          playbackRates: [1, 2, 3],
          preferFullWindow: false,
          responsive: false,
          sources: [Source(url, "video/mp4")],
          suppressNotSupportedError: false),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 29, 30, 37),
      body: SingleChildScrollView(
        scrollDirection: Axis.vertical,
        child: FutureBuilder<Media>(
          future: futureMedia,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              double screenWidth = MediaQuery.of(context).size.width;
              double titleSize = 80;

              if (screenWidth < 800) {
                titleSize = 40;
              }

              return Column(children: [
                Container(
                  padding: const EdgeInsets.fromLTRB(20, 5, 20, 0),
                  child: Text(
                    snapshot.data?.eventName ?? "Photos",
                    style: TextStyle(fontSize: titleSize, color: Colors.white),
                  ),
                ),
                Text(
                  "Organisé par: " + (snapshot.data?.association ?? ""),
                  style: const TextStyle(fontSize: 20, color: Colors.white),
                ),
                PhotoViewer(data: snapshot.data?.medias ?? <MediaData>[])
              ]);
            }

            return const Text("Getting data...");
          },
        ),
      ),
    );
  }
}