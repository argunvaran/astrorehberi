import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../services/api_service.dart';

class SynastryScreen extends StatefulWidget {
  final String lang;
  const SynastryScreen({super.key, required this.lang});

  @override
  State<SynastryScreen> createState() => _SynastryScreenState();
}

class _SynastryScreenState extends State<SynastryScreen> {
  DateTime _d1 = DateTime(1990);
  DateTime _d2 = DateTime(1990);
  TimeOfDay _t1 = const TimeOfDay(hour: 12, minute: 0);
  TimeOfDay _t2 = const TimeOfDay(hour: 12, minute: 0);
  
  bool _loading = false;
  Map<String, dynamic>? _result;
  final ApiService _api = ApiService();

  Future<void> _calc() async {
    setState(() => _loading = true);
    try {
      final t1Str = "${_t1.hour}:${_t1.minute}";
      final t2Str = "${_t2.hour}:${_t2.minute}";
      
      final res = await _api.calculateSynastry(
        date1: _d1, time1: t1Str,
        date2: _d2, time2: t2Str,
        lang: widget.lang
      );
      
      setState(() {
        _result = res;
        _loading = false;
      });
    } catch(e) {
      setState(() => _loading = false);
      if(mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
    }
  }
  
  // Reuse picker logic if possible, or just duplicate for speed
  Future<void> _pickDate(int person) async {
    final init = person == 1 ? _d1 : _d2;
    final picked = await showDatePicker(
      context: context, initialDate: init, firstDate: DateTime(1900), lastDate: DateTime.now(),
      builder: (c, child) => Theme(data: ThemeData.dark().copyWith(colorScheme: const ColorScheme.dark(primary: Colors.pink)), child: child!)
    );
    if(picked != null) setState(() => person == 1 ? _d1 = picked : _d2 = picked);
  }

  Future<void> _pickTime(int person) async {
    final init = person == 1 ? _t1 : _t2;
    final picked = await showTimePicker(
      context: context, initialTime: init,
      builder: (c, child) => Theme(data: ThemeData.dark().copyWith(colorScheme: const ColorScheme.dark(primary: Colors.pink)), child: child!)
    );
    if(picked != null) setState(() => person == 1 ? _t1 = picked : _t2 = picked);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent, elevation: 0,
        title: Text(widget.lang == 'tr' ? "Aşk Uyumu" : "Love Match", style: const TextStyle(fontWeight: FontWeight.bold)),
        leading: BackButton(onPressed: (){
            if(_result != null) setState(() => _result = null);
            else Navigator.pop(context);
        }),
      ),
      body: Container(
        padding: const EdgeInsets.all(20),
         decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter, end: Alignment.bottomCenter,
            colors: [Color(0xFF2E0219), Color(0xFF0F0C29)],
          ),
        ),
        child: SafeArea(
          child: _result != null ? _buildResult() : _buildForm(),
        ),
      ),
    );
  }

  Widget _buildForm() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const SizedBox(height: 20),
        _buildPersonInput(1),
        const SizedBox(height: 20),
        const Icon(Icons.favorite, color: Colors.pinkAccent, size: 40),
        const SizedBox(height: 20),
        _buildPersonInput(2),
        const Spacer(),
        _loading 
          ? const Center(child: CircularProgressIndicator(color: Colors.pink))
          : ElevatedButton(
              onPressed: _calc,
              style: ElevatedButton.styleFrom(backgroundColor: Colors.pink, padding: const EdgeInsets.all(15)),
              child: Text(widget.lang == 'tr' ? "UYUMU HESAPLA" : "CALCULATE COMPATIBILITY", style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
            )
      ],
    ).animate().fadeIn();
  }

  Widget _buildPersonInput(int p) {
    return Container(
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: Colors.white10,
        borderRadius: BorderRadius.circular(15),
        border: Border.all(color: Colors.pinkAccent.withOpacity(0.3))
      ),
      child: Column(
        children: [
          Text(widget.lang == 'tr' ? "$p. Kişi" : "Person $p", style: const TextStyle(color: Colors.white70, fontWeight: FontWeight.bold)),
          const SizedBox(height: 10),
          Row(
            children: [
              Expanded(child: ListTile(
                title: Text("${(p==1?_d1:_d2).day}/${(p==1?_d1:_d2).month}/${(p==1?_d1:_d2).year}", style: const TextStyle(color: Colors.white)),
                trailing: const Icon(Icons.calendar_today, color: Colors.pinkAccent, size: 16),
                onTap: () => _pickDate(p),
              )),
              Expanded(child: ListTile(
                title: Text((p==1?_t1:_t2).format(context), style: const TextStyle(color: Colors.white)),
                trailing: const Icon(Icons.access_time, color: Colors.pinkAccent, size: 16),
                onTap: () => _pickTime(p),
              ))
            ],
          )
        ],
      ),
    );
  }

  Widget _buildResult() {
    final score = _result!['score'] as int;
    final aspects = _result!['aspects'] as List;
    
    return SingleChildScrollView(
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(30),
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              border: Border.all(color: Colors.pink, width: 4),
              color: Colors.pink.withOpacity(0.1)
            ),
            child: Column(
              children: [
                Text("$score%", style: const TextStyle(fontSize: 48, fontWeight: FontWeight.bold, color: Colors.white)),
                Text(widget.lang == 'tr' ? "Uyum" : "Match", style: const TextStyle(color: Colors.white70))
              ],
            ),
          ).animate().scale(duration: 500.ms, curve: Curves.elasticOut),
          const SizedBox(height: 30),
          Text(_result!['summary'] ?? "", style: const TextStyle(color: Colors.white, fontSize: 18, fontStyle: FontStyle.italic), textAlign: TextAlign.center),
          const SizedBox(height: 30),
          // Aspects List
          ...aspects.map((a) => Container(
            margin: const EdgeInsets.only(bottom: 10),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.05),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.white10),
            ),
            child: ExpansionTile(
              title: Text(
                "${a['p1']} ${a['type']} ${a['p2']}", 
                style: const TextStyle(color: Colors.pinkAccent, fontWeight: FontWeight.bold)
              ),
              subtitle: Text(
                a['theme'] ?? "", 
                style: const TextStyle(color: Colors.white70, fontSize: 12)
              ),
              iconColor: Colors.pinkAccent,
              collapsedIconColor: Colors.white54,
              children: [
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Text(
                    a['text'] ?? (widget.lang == 'tr' ? "Yorum bulunamadı." : "No interpretation found."),
                    style: const TextStyle(color: Colors.white),
                  ),
                )
              ],
            ),
          ))
        ],
      ),
    );
  }
}
