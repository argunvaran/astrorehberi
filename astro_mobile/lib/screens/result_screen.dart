import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/chart_model.dart';
import 'dart:math' as math;
import '../theme/strings.dart';

class ChartPainter extends CustomPainter {
  final List<Planet> planets;
  ChartPainter(this.planets);

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2;
    final paint = Paint()
      ..color = Colors.white.withOpacity(0.1)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.0;

    // Draw Wheel circles
    canvas.drawCircle(center, radius, paint);
    canvas.drawCircle(center, radius * 0.8, paint);

    // Draw Houses (Simple lines)
    for (int i = 0; i < 12; i++) {
        final angle = (i * 30) * (math.pi / 180);
        final p2 = Offset(
            center.dx + radius * math.cos(angle),
            center.dy + radius * math.sin(angle)
        );
        canvas.drawLine(center, p2, paint);
    }

    // Draw Planets (Simplified)
    final textPainter = TextPainter(textDirection: TextDirection.ltr);
    for (var p in planets) {
        // Simple equal spacing logic or usage of p.lon if accurate drawing needed
        // For visual flair we just distribute them or use lon
        // Flutter coordinate system: 0 is right (3 o'clock), Astrology 0 Aries is usually 9 o'clock or 3 o'clock depending on chart style.
        // Let's assume standard math angle for simplicity.
        final angle = (p.lon) * (math.pi / 180); 
        // We might want to adjust starting point. 
        
        final pPos = Offset(
            center.dx + (radius * 0.65) * math.cos(angle),
            center.dy + (radius * 0.65) * math.sin(angle)
        );
        
        // Draw Planet Dot
        canvas.drawCircle(pPos, 4, Paint()..color = const Color(0xFFE94560));
        
        // Label
        textPainter.text = TextSpan(
            text: p.name.substring(0, 2), 
            style: const TextStyle(color: Colors.white, fontSize: 10)
        );
        textPainter.layout();
        textPainter.paint(canvas, Offset(pPos.dx - 5, pPos.dy - 5));
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}


class ResultScreen extends StatelessWidget {
  final ChartData data;
  final String lang;

  const ResultScreen({super.key, required this.data, required this.lang});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(AppStrings.get('chart_title', lang), style: GoogleFonts.cinzel(fontWeight: FontWeight.bold, color: const Color(0xFFFFD700))),
        backgroundColor: const Color(0xFF0F0C29),
        elevation: 0,
        centerTitle: true,
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF0F0C29), Color(0xFF302B63), Color(0xFF24243E)],
          ),
        ),
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
               // Chart Wheel
               SizedBox(
                height: 300,
                width: 300,
                child: CustomPaint(painter: ChartPainter(data.planets)),
               ).animate().scale(duration: 600.ms),
               
               const SizedBox(height: 30),
               
               // Cosmic Fingerprint (Planets)
               Text("Your Cosmic Fingerprint", style: GoogleFonts.cinzel(fontSize: 22, color: const Color(0xFFFFD700))),
               const SizedBox(height: 10),
               ...data.planets.map((p) => _buildPlanetTile(p)).toList(),
               
               const SizedBox(height: 30),
               
               // Aspects
               Text(AppStrings.get('aspects_title', lang), style: GoogleFonts.cinzel(fontSize: 22, color: const Color(0xFFFFD700))),
               const SizedBox(height: 10),
               ...data.aspects.map((a) => Container(
                 margin: const EdgeInsets.only(bottom: 10),
                 decoration: BoxDecoration(color: Colors.white.withOpacity(0.05), borderRadius: BorderRadius.circular(10)),
                 child: ListTile(
                   title: Text("${a.p1} - ${a.p2}", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                   subtitle: Text(a.interpretation, style: const TextStyle(color: Colors.white70)),
                   leading: const Icon(Icons.compare_arrows, color: Colors.amber),
                 ),
               )).toList()
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildPlanetTile(Planet p) {
    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: Colors.white10),
      ),
      child: ListTile(
        title: Text("${p.name} in ${p.sign}", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        subtitle: Text(p.interpretation, style: const TextStyle(color: Colors.white70)),
        leading: CircleAvatar(
          backgroundColor: Colors.white10,
          child: Text(
            p.name.isNotEmpty ? p.name[0] : "?", 
            style: const TextStyle(color: Colors.white),
          ),
        ), 
      ),
    );
  }
}
