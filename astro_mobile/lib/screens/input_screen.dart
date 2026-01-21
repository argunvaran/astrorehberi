import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../models/chart_model.dart';
import '../services/api_service.dart';
import 'result_screen.dart';
import 'daily_screen.dart';
import 'social_screen.dart'; 
import 'tarot_screen.dart';
import 'synastry_screen.dart';
import 'draconic_screen.dart';
import 'hours_screen.dart';
import 'landing_screen.dart';

import '../theme/strings.dart';

class InputScreen extends StatefulWidget {
  const InputScreen({super.key});

  @override
  State<InputScreen> createState() => _InputScreenState();
}

class _InputScreenState extends State<InputScreen> {
  final _formKey = GlobalKey<FormState>();
  final ApiService _apiService = ApiService();

  DateTime _selectedDate = DateTime(1990, 1, 1);
  TimeOfDay _selectedTime = const TimeOfDay(hour: 12, minute: 0);
  final TextEditingController _latController = TextEditingController(text: "41.0082"); 
  final TextEditingController _lonController = TextEditingController(text: "28.9784");
  
  bool _isLoading = false;
  String _lang = 'en';

  bool _isAuth = false;
  bool _isAdmin = false;
  bool _formLocked = false;
  String _username = "Guest";

  @override
  void initState() {
    super.initState();
    _checkAuth();
  }

  Future<void> _checkAuth() async {
    final res = await _apiService.checkAuth();
    if (res['authenticated'] == true) {
      if(mounted) {
        setState(() {
          _isAuth = true;
          _isAdmin = res['is_superuser'] == true;
          _username = res['username'] ?? "User";
          // Pre-fill
          if (res['profile'] != null) {
             final p = res['profile'];
             _formLocked = true;
             // Parse date YYYY-MM-DD
             if(p['date'] != null && p['date'].isNotEmpty) {
               try {
                 final parts = p['date'].split('-');
                 _selectedDate = DateTime(int.parse(parts[0]), int.parse(parts[1]), int.parse(parts[2]));
               } catch (_) {}
             }
             // Parse time HH:MM
             if(p['time'] != null && p['time'].isNotEmpty) {
                try {
                  final parts = p['time'].split(':');
                  _selectedTime = TimeOfDay(hour: int.parse(parts[0]), minute: int.parse(parts[1]));
                } catch (_) {}
             }
             _latController.text = p['lat']?.toString() ?? "0";
             _lonController.text = p['lon']?.toString() ?? "0";
          }
        });
      }
    }
  }
  
  Future<void> _logout() async {
    await _apiService.logout();
    if(mounted) {
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const LandingScreen())); // Import LandingScreen
    }
  } 
  
  // ... Keep existing ... 

  // In build method, disable inputs if _formLocked


  void _toggleLanguage() {
    setState(() {
      _lang = _lang == 'en' ? 'tr' : 'en';
    });
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    try {
      final timeStr = "${_selectedTime.hour.toString().padLeft(2, '0')}:${_selectedTime.minute.toString().padLeft(2, '0')}";
      
      final chartData = await _apiService.calculateChart(
        date: _selectedDate,
        time: timeStr,
        lat: double.parse(_latController.text),
        lon: double.parse(_lonController.text),
        lang: _lang,
      );

      if (mounted) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ResultScreen(data: chartData, lang: _lang),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text("${AppStrings.get('error_title', _lang)}: $e"),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Future<void> _pickDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate,
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
      builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
            colorScheme: const ColorScheme.dark(
               primary: Color(0xFFE94560),
               onPrimary: Colors.white,
               surface: Color(0xFF16213E),
               onSurface: Colors.white,
            ),
          ),
          child: child!,
        );
      }
    );
    if (picked != null) setState(() => _selectedDate = picked);
  }

  Future<void> _pickTime() async {
    final picked = await showTimePicker(
      context: context,
      initialTime: _selectedTime,
       builder: (context, child) {
        return Theme(
          data: Theme.of(context).copyWith(
             timePickerTheme: TimePickerThemeData(
               backgroundColor: const Color(0xFF16213E),
               hourMinuteTextColor: Colors.white,
               dayPeriodTextColor: Colors.white,
               dialHandColor: const Color(0xFFE94560),
               dialBackgroundColor: const Color(0xFF1A1A2E),
             )
          ),
          child: child!,
        );
      }
    );
    if (picked != null) setState(() => _selectedTime = picked);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: kIsWeb 
          ? Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const SizedBox(width: 8),
                Image.asset('assets/icon/app_icon.png', height: 40),
                const SizedBox(width: 12),
                Text("DEEP COSMOS", style: GoogleFonts.cinzel(color: const Color.fromARGB(255, 237, 236, 236), fontWeight: FontWeight.bold, fontSize: 24)),
              ],
            ) 
          : const SizedBox.shrink(),
        backgroundColor: Colors.transparent,
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.white), // Drawer icon color
        actions: [
          TextButton.icon(
            onPressed: _toggleLanguage,
            icon: const Icon(Icons.language, color: Color(0xFFE94560)),
            label: Text(
              AppStrings.get('language_btn', _lang), 
              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)
            ),
            style: TextButton.styleFrom(backgroundColor: Colors.black26),
          ),
          const SizedBox(width: 16),
        ],
      ),
      drawer: _buildDrawer(),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Color(0xFF0F0C29), 
              Color(0xFF302B63), 
              Color(0xFF24243E)
            ],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                   const SizedBox(height: 10),
                   Text(
                     AppStrings.get('app_title', _lang),
                     textAlign: TextAlign.center,
                     style: GoogleFonts.cinzel(
                       fontSize: 48,
                       color: const Color(0xFFFFD700),
                       fontWeight: FontWeight.bold,
                       shadows: [
                         const Shadow(blurRadius: 10, color: Colors.amber, offset: Offset(0, 0))
                       ]
                     ),
                   ).animate().fadeIn(duration: 800.ms).slideY(begin: -0.2, end: 0),
                   
                   const SizedBox(height: 10),
                   Text(
                     AppStrings.get('subtitle', _lang),
                     textAlign: TextAlign.center,
                     style: Theme.of(context).textTheme.bodyMedium,
                   ).animate().fadeIn(delay: 300.ms),

                   const SizedBox(height: 50),

                   // Date Picker
                   _buildGlassContainer(
                     child: ListTile(
                       title: Text(AppStrings.get('date_label', _lang), style: const TextStyle(color: Colors.white70)),
                       subtitle: Text(
                         "${_selectedDate.day}/${_selectedDate.month}/${_selectedDate.year}",
                         style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
                       ),
                       trailing: const Icon(Icons.calendar_today, color: Color(0xFFE94560)),
                       onTap: _formLocked ? null : _pickDate,
                     ),
                   ).animate().fadeIn(delay: 400.ms).slideX(),

                   const SizedBox(height: 16),

                   // Time Picker
                   _buildGlassContainer(
                     child: ListTile(
                       title: Text(AppStrings.get('time_label', _lang), style: const TextStyle(color: Colors.white70)),
                       subtitle: Text(
                         _selectedTime.format(context),
                         style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
                       ),
                       trailing: Icon(Icons.access_time, color: _formLocked ? Colors.grey : const Color(0xFFE94560)),
                       onTap: _formLocked ? null : _pickTime,
                     ),
                   ).animate().fadeIn(delay: 500.ms).slideX(),

                   const SizedBox(height: 16),
                   
                   // Location
                    Row(
                      children: [
                        Expanded(
                          child: TextFormField(
                            controller: _latController,
                            enabled: !_formLocked,
                            decoration: InputDecoration(
                              labelText: AppStrings.get('lat_label', _lang), 
                              suffixIcon: const Icon(Icons.location_on_outlined, color: Colors.white54)
                            ),
                            keyboardType: TextInputType.number,
                            style: const TextStyle(color: Colors.white),
                            validator: (v) => v!.isEmpty ? 'Required' : null,
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: TextFormField(
                            controller: _lonController,
                            enabled: !_formLocked,
                            decoration: InputDecoration(
                              labelText: AppStrings.get('lon_label', _lang), 
                              suffixIcon: const Icon(Icons.location_on_outlined, color: Colors.white54)
                            ),
                            keyboardType: TextInputType.number,
                            style: const TextStyle(color: Colors.white),
                            validator: (v) => v!.isEmpty ? 'Required' : null,
                          ),
                        ),
                      ],
                    ).animate().fadeIn(delay: 600.ms),

                   const Spacer(),

                   _isLoading 
                   ? const Center(child: CircularProgressIndicator(color: Color(0xFFE94560)))
                   : ElevatedButton(
                     onPressed: _submit,
                     child: Text(AppStrings.get('btn_generate', _lang)),
                   ).animate().fadeIn(delay: 700.ms).scale(),
                   
                   const SizedBox(height: 20),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildDrawer() {
    final bool isTr = _lang == 'tr';
    return Drawer(
      child: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft, end: Alignment.bottomRight,
            colors: [Color(0xFF1a0b2e), Color(0xFF4a148c)],
          ),
        ),
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: const BoxDecoration(
                border: Border(bottom: BorderSide(color: Colors.white24)),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.auto_awesome, color: Color(0xFFFFD700), size: 50),
                  const SizedBox(height: 10),
                  Text("DEEP COSMOS", style: GoogleFonts.cinzel(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
                  if(_isAuth)
                  Padding(
                    padding: const EdgeInsets.only(top: 5),
                    child: Text(_username, style: const TextStyle(color: Color(0xFFE94560), fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
            ),
            _drawerItem(Icons.star, isTr ? "Natal Harita" : "Natal Chart", () => Navigator.pop(context)),
            _drawerItem(Icons.calendar_month, isTr ? "Günlük & Haftalık" : "Daily & Weekly", () => Navigator.push(context, MaterialPageRoute(builder: (_) => DailyScreen(lang: _lang)))),
            _drawerItem(Icons.groups, isTr ? "Sosyal Analiz" : "Social Analysis", () => Navigator.push(context, MaterialPageRoute(builder: (_) => SocialScreen(lang: _lang)))),
            const Divider(color: Colors.white24),
            _drawerItem(Icons.favorite, isTr ? "Aşk Uyumu (Synastry)" : "Love Match", () => Navigator.push(context, MaterialPageRoute(builder: (_) => SynastryScreen(lang: _lang)))),
            _drawerItem(Icons.fingerprint, isTr ? "Drakonik Ruh" : "Draconic Soul", () => Navigator.push(context, MaterialPageRoute(builder: (_) => DraconicScreen(lang: _lang)))),
            _drawerItem(Icons.access_time_filled, isTr ? "Gezegen Saatleri" : "Planetary Hours", () => Navigator.push(context, MaterialPageRoute(builder: (_) => HoursScreen(lang: _lang)))),
            const Divider(color: Colors.white24),
            _drawerItem(Icons.style, isTr ? "Mistik Tarot" : "Mystic Tarot", () => Navigator.push(context, MaterialPageRoute(builder: (_) => TarotScreen(lang: _lang))), highlight: true),
            
            if (_isAdmin)
              _drawerItem(Icons.admin_panel_settings, "Kozmik Panel", () {
                 // Open Web Admin in browser since native is not built
                 // Or show Dialog "Please use web for admin features"
                 ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Admin Panel is Web-Only for now")));
              }, highlight: true),

            const Spacer(),
            if(_isAuth)
             ListTile(
              leading: const Icon(Icons.logout, color: Colors.redAccent),
              title: Text(isTr ? "Çıkış Yap" : "Logout", style: const TextStyle(color: Colors.redAccent)),
              onTap: _logout,
            ),
          ],
        ),
      ),
    );
  }

  Widget _drawerItem(IconData icon, String title, VoidCallback onTap, {bool highlight = false}) {
    return ListTile(
      leading: Icon(icon, color: highlight ? const Color(0xFFFFD700) : Colors.white70),
      title: Text(title, style: TextStyle(color: highlight ? const Color(0xFFFFD700) : Colors.white, fontWeight: highlight ? FontWeight.bold : FontWeight.normal)),
      onTap: onTap,
    );
  }

  Widget _buildGlassContainer({required Widget child}) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white.withOpacity(0.1)),
      ),
      child: child,
    );
  }
}
