import 'package:flutter/material.dart';
import 'package:video_js/video_js.dart';

import './pages/home.dart';
import 'pages/event_photos.dart';
import 'pages/AI_photos.dart';

// run with:    flutter run -d edge
// build with:  flutter build web --release -v
//    build is stored in: build/web/

void main() {
  VideoJsResults().init();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see the
        // application has a blue toolbar. Then, without quitting the app, try
        // changing the primarySwatch below to Colors.green and then invoke
        // "hot reload" (press "r" in the console where you ran "flutter run",
        // or simply save your changes to "hot reload" in a Flutter IDE).
        // Notice that the counter didn't reset back to zero; the application
        // is not restarted.
        primarySwatch: Colors.blue,
      ),
      onGenerateRoute: (settings) {
        // Handle '/'
        if (settings.name == '/') {
          return MaterialPageRoute(
              settings: settings, builder: (context) => const HomePage());
        }

        var uri = Uri.parse(settings.name ?? "");

        // Handle '/photos/:path'
        if (uri.pathSegments.first == 'photos') {
          var url = "";

          for (String path in uri.pathSegments) {
            url += path + '/';
          }

          return MaterialPageRoute(
              settings: settings, builder: (context) => PhotosPage(url: url));
        }

        // Handle '/IA/:name'
        if (uri.pathSegments.first == 'IA') {
          return MaterialPageRoute(
              settings: settings,
              builder: (context) => AiPhotosPage(name: uri.pathSegments[1]));
        }

        // Handles everything else
        return MaterialPageRoute(
            settings: settings,
            builder: (context) => HomePage()); // Maybe a 404
      },
    );
  }
}
