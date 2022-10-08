import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late ScrollController
      _scrollController; // used to create the snapping scroll effect

  @override
  void initState() {
    _scrollController = ScrollController();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      body: Listener(
        onPointerSignal: (pointerSignal) {
          if (pointerSignal is PointerScrollEvent) {
            var whereTo = pointerSignal.scrollDelta.dy.abs() /
                pointerSignal.scrollDelta.dy;
            var current =
                (_scrollController.offset / screenHeight)
                    .round();
            _scrollController.animateTo(
                screenHeight * (current + whereTo),
                duration: const Duration(milliseconds: 500),
                curve: Curves.easeInOut);
          }
        },
        child: ListView(
          shrinkWrap: true,
          controller: _scrollController,
          physics: const NeverScrollableScrollPhysics(),
          children: [
            /* 
              Homepage, with sublinks
            */
            Container(
              height: screenHeight,
              width: screenWidth,
              padding: const EdgeInsets.all(10),
              //color: Colors.grey.shade900,
              // First background image
              decoration: const BoxDecoration(
                image: DecorationImage(
                    //opacity: .4,
                    colorFilter: ColorFilter.matrix(<double>[
                      0.2,
                      0.2,
                      0.2,
                      0,
                      0,
                      0.2,
                      0.2,
                      0.2,
                      0,
                      0,
                      0.2,
                      0.2,
                      0.2,
                      0,
                      0,
                      0,
                      0,
                      0,
                      1,
                      0,
                    ]),
                    image: AssetImage("images/paysage.jpg"),
                    fit: BoxFit.cover),
              ),
              child: Stack(
                fit: StackFit.expand,
                children: [
                  Container(
                    alignment: Alignment.topCenter,
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        TextButton(
                          onPressed: () {
                            _scrollController.animateTo(
                                screenHeight,
                                duration: const Duration(milliseconds: 500),
                                curve: Curves.easeInOut);
                          },
                          child: const Text(
                            "Dernières photos",
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 30,
                            ),
                          ),
                        ),
                        TextButton(
                          onPressed: () {
                            _scrollController.animateTo(
                                screenHeight * 2,
                                duration: const Duration(milliseconds: 500),
                                curve: Curves.easeInOut);
                          },
                          child: const Text(
                            "L'équipe",
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 30,
                            ),
                          ),
                        ),
                        const Text(
                          "MiTV",
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 80,
                          ),
                        ),
                        TextButton(
                          onPressed: () {
                            _scrollController.animateTo(
                                screenHeight * 3,
                                duration: const Duration(milliseconds: 500),
                                curve: Curves.easeInOut);
                          },
                          child: const Text(
                            "Le matériel",
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 30,
                            ),
                          ),
                        ),
                        TextButton(
                          onPressed: () {
                            _scrollController.animateTo(
                                screenHeight * 4,
                                duration: const Duration(milliseconds: 500),
                                curve: Curves.easeInOut);
                          },
                          child: const Text(
                            "Mention légales",
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 30,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  UnconstrainedBox(
                    alignment: Alignment.centerRight,
                    child: Container(
                      margin: const EdgeInsets.fromLTRB(0, 100, 50, 0),
                      width: screenWidth/3,
                      height: screenWidth/3,
                      child: Image.asset(
                        "images/soiree.jpg",
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                  UnconstrainedBox(
                    alignment: Alignment.centerRight,
                    child: Container(
                      margin: EdgeInsets.fromLTRB(0, 100, 50 + screenWidth/5, 0),
                      width: screenWidth/3,
                      height: screenWidth/4,
                      child: Image.asset(
                        "images/perm.jpg",
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                  Container(
                    alignment: Alignment.bottomLeft,
                    margin: const EdgeInsets.fromLTRB(50, 0, 0, 50),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        const Text(
                          "Rendre vos\nsoirées\nmémorables",
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 65,
                          ),
                        ),
                        const SizedBox(
                          height: 100,
                        ),
                        TextButton(
                          onPressed: () {
                            Navigator.pushNamed(context, '/photos');
                          },
                          child: const Text(
                            "Voir les photos",
                            style: TextStyle(
                              color: Color.fromARGB(255, 119, 211, 247),
                              fontSize: 45,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            /*
              Photos section
            */
            Container(
              height: screenHeight,
              width: screenWidth,
              padding: const EdgeInsets.all(50),
              color: Color.fromARGB(255, 24, 25, 29),
              child: Stack(
                fit: StackFit.expand,
                children: [
                  UnconstrainedBox(
                    alignment: Alignment.centerRight,
                    child: Container(
                      margin: const EdgeInsets.fromLTRB(0, 0, 0, 0),
                      width: 800,
                      height: 800,
                      child: Image.asset(
                        "images/soiree.jpg",
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                  UnconstrainedBox(
                    alignment: Alignment.centerRight,
                    child: Container(
                      margin: const EdgeInsets.fromLTRB(0, 0, 700, 0),
                      width: 700,
                      height: 600,
                      child: Image.asset(
                        "images/perm.jpg",
                        fit: BoxFit.cover,
                      ),
                    ),
                  ),
                  Container(
                    alignment: Alignment.bottomLeft,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        const Text(
                          "Rendre vos\nsoirées\nmémorables",
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 65,
                          ),
                        ),
                        const SizedBox(
                          height: 100,
                        ),
                        TextButton(
                          onPressed: () {
                            Navigator.pushNamed(context, '/photos');
                          },
                          child: const Text(
                            "Voir les photos",
                            style: TextStyle(
                              color: Color.fromARGB(255, 119, 211, 247),
                              fontSize: 45,
                            ),
                          ),
                        ),
                      ],
                    ),
                  )
                ],
              ),
            ),
            /*
              Team section
            */
            Container(
              height: screenHeight,
              width: screenWidth,
              padding: const EdgeInsets.all(50),
              color: Color.fromARGB(255, 50, 52, 58),
              child: Stack(
                fit: StackFit.expand,
                children: [],
              ),
            ),
            /*
              Legal section
            */
            Container(
              height: screenHeight,
              width: screenWidth,
              padding: const EdgeInsets.all(50),
              color: Color.fromARGB(255, 31, 32, 36),
              child: Stack(
                fit: StackFit.expand,
                children: [
                  const Text(
                      "Vous autorisez MiTV a conserver vos photos ainsi que votre nom et prénom")
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
