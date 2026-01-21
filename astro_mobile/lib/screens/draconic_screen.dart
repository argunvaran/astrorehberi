import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/chart_model.dart';
import '../services/api_service.dart';

class DraconicScreen extends StatefulWidget {
  final String lang;
  const DraconicScreen({super.key, required this.lang});

  @override
  State<DraconicScreen> createState() => _DraconicScreenState();
}

class _DraconicScreenState extends State<DraconicScreen> {
  DateTime _date = DateTime(1990);
  TimeOfDay _time = const TimeOfDay(hour: 12, minute: 0);
  final _latCtrl = TextEditingController(text: "41.0");
  final _lonCtrl = TextEditingController(text: "28.0");
  bool _loading = false;
  ChartData? _data;
  final ApiService _api = ApiService();

  Future<void> _calc() async {
    setState(() => _loading = true);
    try {
      final t = "${_time.hour}:${_time.minute}";
      final res = await _api.calculateChart(
        date: _date, time: t,
        lat: double.parse(_latCtrl.text),
        lon: double.parse(_lonCtrl.text),
        lang: widget.lang
      );
      setState(() {
        _data = res;
        _loading = false;
      });
    } catch(e) {
      setState(() => _loading = false);
      if(mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.lang == 'tr' ? "Drakonik Ruh" : "Draconic Soul", style: TextStyle(color: Colors.cyanAccent)),
        backgroundColor: Colors.transparent, elevation: 0,
        leading: BackButton(onPressed: (){
            if(_data != null) setState(() => _data = null);
            else Navigator.pop(context);
        }),
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
              begin: Alignment.topRight, end: Alignment.bottomLeft,
              colors: [Color(0xFF001f3f), Color(0xFF000000)]),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: _data != null ? _buildResult() : _buildForm(),
          ),
        ),
      ),
    );
  }

  Widget _buildForm() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Text("Discover your higher self's coding...", style: TextStyle(color: Colors.cyanAccent, fontSize: 16), textAlign: TextAlign.center),
        const SizedBox(height: 30),
        ListTile(
          title: Text("${_date.day}/${_date.month}/${_date.year}", style: TextStyle(color: Colors.white)),
          trailing: Icon(Icons.calendar_today, color: Colors.cyan),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10), side: BorderSide(color: Colors.white24)),
          onTap: () async {
             final d = await showDatePicker(context: context, initialDate: _date, firstDate: DateTime(1900), lastDate: DateTime.now());
             if(d!=null) setState(()=>_date=d);
          },
        ),
        const SizedBox(height: 10),
        ListTile(
          title: Text(_time.format(context), style: TextStyle(color: Colors.white)),
          trailing: Icon(Icons.access_time, color: Colors.cyan),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10), side: BorderSide(color: Colors.white24)),
          onTap: () async {
             final t = await showTimePicker(context: context, initialTime: _time);
             if(t!=null) setState(()=>_time=t);
          },
        ),
        const SizedBox(height: 20),
        if(_loading) const Center(child: CircularProgressIndicator(color: Colors.cyan))
        else ElevatedButton.icon(
          onPressed: _calc,
          icon: Icon(Icons.fingerprint),
          label: Text("REVEAL SOUL CONTRACT"),
          style: ElevatedButton.styleFrom(backgroundColor: Colors.cyan, foregroundColor: Colors.black),
        )
      ],
    ).animate().fadeIn();
  }

  Widget _buildResult() {
     final meta = _data?.meta;
     if(meta == null || meta.draconicChart.isEmpty) {
       return const Center(child: Text("No Draconic Data Found", style: TextStyle(color: Colors.white)));
     }
     
     return ListView.builder(
       itemCount: meta.draconicChart.length,
       itemBuilder: (context, index) {
         final p = meta.draconicChart[index];
         return Container(
           margin: const EdgeInsets.only(bottom: 15),
           padding: const EdgeInsets.all(16),
           decoration: BoxDecoration(
             color: Colors.white.withOpacity(0.05),
             borderRadius: BorderRadius.circular(16),
             border: Border.all(color: Colors.cyan.withOpacity(0.3))
           ),
           child: Column(
             crossAxisAlignment: CrossAxisAlignment.start,
             children: [
               Row(
                 mainAxisAlignment: MainAxisAlignment.spaceBetween,
                 children: [
                   Text(p['name'] ?? "", style: GoogleFonts.cinzel(color: Colors.cyanAccent, fontSize: 18, fontWeight: FontWeight.bold)),
                   Container(
                     padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                     decoration: BoxDecoration(color: Colors.cyan.withOpacity(0.2), borderRadius: BorderRadius.circular(20)),
                     child: Text(p['sign'] ?? "", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                   )
                 ],
               ),
               const SizedBox(height: 10),
               Text(p['interpretation'] ?? "", style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.5)),
             ],
           ),
         ).animate().fadeIn(delay: (index * 100).ms).slideY(begin: 0.1, end: 0);
       },
     );
  }

  Widget _buildDraconicList() {
      return _buildResult();
  }
}
