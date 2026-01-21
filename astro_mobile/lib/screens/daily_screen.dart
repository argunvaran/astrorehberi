import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/api_service.dart';
import '../models/chart_model.dart'; // Reusing for consistent models if necessary
import 'dart:convert';
import 'package:home_widget/home_widget.dart';

class DailyScreen extends StatefulWidget {
  final String lang;
  const DailyScreen({super.key, required this.lang});

  @override
  State<DailyScreen> createState() => _DailyScreenState();
}

class _DailyScreenState extends State<DailyScreen> {
  Map<String, dynamic>? dailyData;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    try {
      final data = await ApiService.getDailyPlanner(widget.lang);
      setState(() {
        dailyData = data;
        isLoading = false;
      });
      
      // Update Widget
      await _updateWidget(data);
      
    } catch (e) {
      setState(() => isLoading = false);
      print(e);
    }
  }

  Future<void> _updateWidget(Map<String, dynamic> data) async {
    try {
        await HomeWidget.saveWidgetData<String>('phase', data['phase']);
        // Get first tip if available
        String advice = "Check app for daily tips";
        if (data['tips'] != null && (data['tips'] as List).isNotEmpty) {
            advice = (data['tips'] as List).first;
        }
        await HomeWidget.saveWidgetData<String>('advice', advice);
        await HomeWidget.updateWidget(
            name: 'AstroWidget',
            androidName: 'AstroWidget',
        );
    } catch (e) {
        print("Widget Update Failed: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Daily Cosmic Guide", style: GoogleFonts.cinzel(color: const Color(0xFFFFD700))),
        backgroundColor: const Color(0xFF0F0C29),
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF0F0C29), Color(0xFF302B63), Color(0xFF24243E)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: isLoading 
            ? const Center(child: CircularProgressIndicator(color: Color(0xFFE94560)))
            : SingleChildScrollView(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Moon Phase Header
                    Center(
                      child: Column(
                        children: [
                          Icon(Icons.nightlight_round, size: 80, color: Colors.amber.shade200)
                              .animate(onPlay: (c) => c.repeat(reverse: true))
                              .scaleXY(end: 1.1, duration: 2.seconds),
                          const SizedBox(height: 10),
                          Text(dailyData?['phase'] ?? 'Moon Phase', 
                              style: GoogleFonts.cinzel(fontSize: 28, color: Colors.white, fontWeight: FontWeight.bold)),
                          Text("Current Lunar Phase", style: TextStyle(color: Colors.white54)),
                        ],
                      ),
                    ),
                    const SizedBox(height: 30),

                    // Retrogrades Warning
                    if (dailyData?['retrogrades'] != null && (dailyData!['retrogrades'] as List).isNotEmpty)
                      Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(16),
                        margin: const EdgeInsets.only(bottom: 20),
                        decoration: BoxDecoration(
                          color: Colors.red.withOpacity(0.1),
                          border: Border.all(color: Colors.red.withOpacity(0.5)),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                             const Row(children: [
                               Icon(Icons.warning_amber_rounded, color: Colors.redAccent),
                               SizedBox(width: 8),
                               Text("Retrograde Alert", style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold, fontSize: 18))
                             ]),
                             const SizedBox(height: 10),
                             ...(dailyData!['retrogrades'] as List).map((p) => Text(
                               "• $p is currently retrograde.", style: const TextStyle(color: Colors.white70)
                             )).toList()
                          ],
                        ),
                      ).animate().shake(duration: 500.ms),

                    // Tips
                    Text("Daily Advice", style: GoogleFonts.cinzel(fontSize: 22, color: Colors.white)),
                    const SizedBox(height: 10),
                    ListView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      itemCount: (dailyData?['tips'] as List?)?.length ?? 0,
                      itemBuilder: (ctx, i) {
                        return Container(
                          margin: const EdgeInsets.only(bottom: 10),
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.05),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(color: Colors.white.withOpacity(0.1)),
                          ),
                          child: Row(
                            children: [
                              const Icon(Icons.star, color: Color(0xFFE94560)),
                              const SizedBox(width: 15),
                              Expanded(
                                child: Text(dailyData!['tips'][i], style: const TextStyle(color: Colors.white, fontSize: 16))
                              )
                            ],
                          ),
                        ).animate().fadeIn(delay: (100*i).ms).slideX();
                      },
                    )
                  ],
                ),
              ),
      ),
    );
  }
}
