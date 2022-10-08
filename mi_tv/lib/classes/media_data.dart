class Media {
  final String eventName;
  final String association;
  final List<MediaData> medias;

  const Media(
      {required this.medias,
      required this.eventName,
      required this.association});

  factory Media.fromJson(Map<String, dynamic> json) {
    final List<MediaData> _medias = <MediaData>[];
    String _eventName = "";
    String _association = "";

    json.forEach((key, value) {
      if (key == "event_name") {
        _eventName = value;
      } else if (key == "association") {
        _association = value;
      } else if (value['type'] == "dir") {
        _medias.add(MediaData(
            url: key,
            type: value['type'],
            thumbnail: value['thumbnail'],
            excludeThumbnail: value['exlude_thumbnail'],
            eventName: value['event_name'],
            association: value['association']));
      } else {
        _medias.add(MediaData(url: key, type: value['type']));
      }
    });

    return Media(
        medias: _medias, eventName: _eventName, association: _association);
  }
}

class MediaData {
  final String url;
  final String type;
  final String thumbnail;
  final String excludeThumbnail;
  final String eventName;
  final String association;

  const MediaData({
    required this.url,
    required this.type,
    this.thumbnail = "",
    this.excludeThumbnail = "",
    this.eventName = "",
    this.association = "",
  });
}