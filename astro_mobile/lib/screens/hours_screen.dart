import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../services/api_service.dart';

class HoursScreen extends StatefulWidget {
  final String lang;
  const HoursScreen({super.key, required this.lang});

  @override
  State<HoursScreen> createState() => _HoursScreenState();
}

class _HoursScreenState extends State<HoursScreen> {
  Map<String, dynamic>? _data;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _fetch();
  }

  Future<void> _fetch() async {
    try {
      final res = await ApiService.getDailyPlanner(widget.lang);
      setState(() {
        _data = res;
        _loading = false;
      });
    } catch (e) {
      setState(() => _loading = false);
      if(mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
    }
  }

  @override
  Widget build(BuildContext context) {
    final isTr = widget.lang == 'tr';
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: Text(isTr ? "Gezegen Saatleri" : "Planetary Hours", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: const BackButton(color: Colors.white),
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter, end: Alignment.bottomCenter,
            colors: [Color(0xFF0F0C29), Color(0xFF302B63)],
          ),
        ),
        child: SafeArea(
          child: _loading 
             ? const Center(child: CircularProgressIndicator(color: Colors.amber))
             : _buildList(),
        ),
      ),
    );
  }

  Widget _buildList() {
    final hours = _data?['hours'] as List? ?? [];
    if(hours.isEmpty) return const Center(child: Text("No Data", style: TextStyle(color: Colors.white)));

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: hours.length,
      itemBuilder: (context, index) {
        final h = hours[index];
        final planet = h['planet'];
        final color = _getPlanetColor(planet);
        return Container(
          margin: const EdgeInsets.only(bottom: 12),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.05),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.white10),
          ),
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: color.withOpacity(0.2),
              child: Text(planet[0], style: TextStyle(color: color, fontWeight: FontWeight.bold)),
            ),
            title: Text(planet, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
            subtitle: Text("${h['start']} - ${h['end']}", style: const TextStyle(color: Colors.white70)),
            trailing: const Icon(Icons.access_time, color: Colors.white24),
          ),
        ).animate().fadeIn(delay: (index * 50).ms).slideX();
      },
    );
  }

  Color _getPlanetColor(String p) {
    if(p.contains("Sun") || p.contains("Güneş")) return Colors.orange;
    if(p.contains("Moon") || p.contains("Ay")) return Colors.grey;
    if(p.contains("Mars")) return Colors.red;
    if(p.contains("Mercury") || p.contains("Merkür")) return Colors.blueGrey;
    if(p.contains("Jupiter") || p.contains("Jüpiter")) return Colors.purple;
    if(p.contains("Venus") || p.contains("Venüs")) return Colors.pinkAccent;
    if(p.contains("Saturn") || p.contains("Satürn")) return Colors.brown;
    return Colors.white;
  }
}
