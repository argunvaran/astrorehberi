import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';
import '../services/api_service.dart';
import '../models/chart_model.dart';

class SocialScreen extends StatefulWidget {
  final String lang;
  
  const SocialScreen({super.key, required this.lang});

  @override
  State<SocialScreen> createState() => _SocialScreenState();
}

class _SocialScreenState extends State<SocialScreen> {
  final List<Map<String, dynamic>> members = [];
  bool isLoading = false;
  Map<String, int>? groupBalance;
  
  // Color palette
  final Color bgDark = const Color(0xFF0F0C29);
  final Color accent = const Color(0xFFE94560);
  final Color cardBg = Colors.white.withOpacity(0.05);

  Future<void> _addMember(String name, String date) async {
    setState(() => isLoading = true);
    try {
      // API Call
      // Helper: we need a way to call calculateChart directly.
      // We will construct the payload manually here or assume ApiService exposes it.
      // Since ApiService.calculateChart is static, we can use it.
      
      final api = ApiService();
      // Parse inputs
      final dateParts = date.split('/');
      final dt = DateTime(int.parse(dateParts[0]), int.parse(dateParts[1]), int.parse(dateParts[2]));
      
      final data = await api.calculateChart(
        date: dt,
        time: '12:00',
        lat: 41.0, 
        lon: 28.0,
        lang: widget.lang
      );
      
      final dominants = data.meta?.dominants ?? {};
      
      setState(() {
        members.add({
          'name': name,
          'dominants': dominants,
        });
        groupBalance = null; // Reset analysis
        isLoading = false;
      });
      
    } catch (e) {
      setState(() => isLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
    }
  }

  void _analyzeGroup() {
    if (members.isEmpty) return;
    
    final totals = {'Fire': 0, 'Earth': 0, 'Air': 0, 'Water': 0};
    
    for (var m in members) {
      final dom = m['dominants'] as Map<String, dynamic>;
      totals['Fire'] = (totals['Fire']! + (dom['Fire'] ?? 0)).toInt();
      totals['Earth'] = (totals['Earth']! + (dom['Earth'] ?? 0)).toInt();
      totals['Air'] = (totals['Air']! + (dom['Air'] ?? 0)).toInt();
      totals['Water'] = (totals['Water']! + (dom['Water'] ?? 0)).toInt();
    }
    
    // Average
    final count = members.length;
    setState(() {
      groupBalance = {
        'Fire': (totals['Fire']! / count).round(),
        'Earth': (totals['Earth']! / count).round(),
        'Air': (totals['Air']! / count).round(),
        'Water': (totals['Water']! / count).round(),
      };
    });
  }

  void _showAddDialog() {
    final nameCtrl = TextEditingController();
    final dateCtrl = TextEditingController(text: "1995/05/05");
    
    showDialog(
      context: context, 
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF302B63),
        title: Text("Add Member", style: GoogleFonts.cinzel(color: Colors.white)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
               controller: nameCtrl,
               style: const TextStyle(color: Colors.white),
               decoration: const InputDecoration(labelText: "Name", labelStyle: TextStyle(color: Colors.white70)),
            ),
            TextField(
               controller: dateCtrl,
               style: const TextStyle(color: Colors.white),
               decoration: const InputDecoration(labelText: "YYYY/MM/DD", labelStyle: TextStyle(color: Colors.white70)),
            ),
          ],
        ),
        actions: [
          TextButton(
            child: const Text("Cancel"),
            onPressed: () => Navigator.pop(ctx),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: accent),
            child: const Text("Add"),
            onPressed: () {
               if(nameCtrl.text.isNotEmpty) {
                 Navigator.pop(ctx);
                 _addMember(nameCtrl.text, dateCtrl.text);
               }
            },
          )
        ],
      )
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Social Analysis", style: GoogleFonts.cinzel(color: const Color(0xFFFFD700))),
        backgroundColor: bgDark,
        centerTitle: true,
        actions: [
          IconButton(icon: const Icon(Icons.add_circle, color: Colors.green), onPressed: _showAddDialog)
        ],
      ),
      body: Container(
        decoration: BoxDecoration(
           gradient: LinearGradient(
              begin: Alignment.topCenter, end: Alignment.bottomCenter,
              colors: [bgDark, const Color(0xFF24243E)]
           )
        ),
        child: Column(
           children: [
              // Member List
              Expanded(
                flex: 2,
                child: members.isEmpty 
                  ? Center(child: Text("No members yet.", style: GoogleFonts.poppins(color: Colors.white54)))
                  : ListView.builder(
                      padding: const EdgeInsets.all(16),
                      itemCount: members.length,
                      itemBuilder: (ctx, i) {
                         final m = members[i];
                         final dom = m['dominants'] as Map<String, dynamic>;
                         // Find highest
                         String maxEl = "Fire";
                         num maxVal = 0;
                         dom.forEach((k, v) { if(v > maxVal) { maxVal = v; maxEl = k; } });
                         
                         return Card(
                           color: cardBg,
                           child: ListTile(
                             leading: const CircleAvatar(backgroundColor: Colors.white10, child: Icon(Icons.person, color: Colors.white)),
                             title: Text(m['name'], style: const TextStyle(color: Colors.white)),
                             subtitle: Text("Master of $maxEl", style: TextStyle(color: _getElementColor(maxEl))),
                             trailing: IconButton(icon: const Icon(Icons.delete, color: Colors.red), onPressed: () {
                               setState(() => members.removeAt(i));
                             }),
                           ),
                         ).animate().fadeIn();
                      },
                    ),
              ),
              
              // Analyze Button or Results
              Expanded(
                flex: 3,
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.black26,
                    borderRadius: const BorderRadius.vertical(top: Radius.circular(30)),
                  ),
                  child: Column(
                    children: [
                       if(isLoading) const CircularProgressIndicator(color: Colors.pinkAccent),
                       if(!isLoading) SizedBox(
                         width: double.infinity,
                         child: ElevatedButton.icon(
                            icon: const Icon(Icons.analytics),
                            label: const Text("ANALYZE GROUP DYNAMICS"),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: accent,
                              padding: const EdgeInsets.symmetric(vertical: 15),
                            ),
                            onPressed: _analyzeGroup,
                         ),
                       ),
                       const SizedBox(height: 20),
                       
                       // Results
                       if(groupBalance != null) ...[
                          Text("Group Elemental Balance", style: GoogleFonts.cinzel(color: Colors.white, fontSize: 18)),
                          const SizedBox(height: 20),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceAround,
                            children: groupBalance!.entries.map((e) => Column(
                              children: [
                                Container(
                                  height: 60, width: 60,
                                  decoration: BoxDecoration(
                                    shape: BoxShape.circle,
                                    border: Border.all(color: _getElementColor(e.key), width: 3)
                                  ),
                                  child: Center(child: Text("${e.value}%", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold))),
                                ),
                                const SizedBox(height: 8),
                                Text(e.key, style: const TextStyle(color: Colors.white70))
                              ],
                            )).toList(),
                          ).animate().scale(),
                          
                          const SizedBox(height: 20),
                          const Text("When you are together,", style: TextStyle(color: Colors.white54)),
                          Text(_getGroupInterpretation(groupBalance!), 
                               textAlign: TextAlign.center,
                               style: const TextStyle(color: Colors.white, fontStyle: FontStyle.italic)),
                       ]
                    ],
                  ),
                ),
              )
           ],
        ),
      ),
    );
  }

  Color _getElementColor(String el) {
    if(el == 'Fire') return Colors.orange;
    if(el == 'Water') return Colors.blue;
    if(el == 'Air') return Colors.white;
    if(el == 'Earth') return Colors.green;
    return Colors.grey;
  }
  
  String _getGroupInterpretation(Map<String, int> balance) {
    // Simple logic
    String maxEl = "Fire";
    int maxVal = 0;
    balance.forEach((k, v) { if(v > maxVal) { maxVal = v; maxEl = k; } });
    
    if(maxEl == 'Fire') return "Action, passion, and conflicts rise quickly!";
    if(maxEl == 'Water') return "Emotions run deep; intuition guides the group.";
    if(maxEl == 'Air') return "Ideas flow endlessly; lots of discussion.";
    if(maxEl == 'Earth') return "Practical achievements and stability are focus.";
    return "Balanced energy.";
  }
}
