import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:google_fonts/google_fonts.dart';
import 'dart:math' as math;
import '../models/tarot_model.dart';
import '../services/api_service.dart';

class TarotScreen extends StatefulWidget {
  final String lang;
  const TarotScreen({super.key, required this.lang});

  @override
  State<TarotScreen> createState() => _TarotScreenState();
}

class _TarotScreenState extends State<TarotScreen> with TickerProviderStateMixin {
  // State: 'deck', 'spread', 'revealed'
  String _state = 'deck'; 
  
  // Data
  TarotResponse? _data;
  bool _loading = false;
  
  // Selection
  List<int> _selectedIndices = [];
  final int _totalCards = 22;

  String? _error;

  @override
  void initState() {
    super.initState();
    _fetchData();
  }

  Future<void> _fetchData() async {
    try {
      final res = await ApiService.drawTarot(widget.lang);
      if(mounted) setState(() { _data = res; _error = null; });
    } catch (e) {
      debugPrint("Error fetching tarot: $e");
      if(mounted) setState(() => _error = e.toString());
    }
  }

  void _startSpread() {
    setState(() => _state = 'spread');
  }

  void _selectCard(int index) {
    if (_state != 'spread') return;
    if (_selectedIndices.contains(index)) return;
    if (_selectedIndices.length >= 3) return;

    setState(() {
      _selectedIndices.add(index);
    });
  }

  void _reveal() {
    if (_data == null) {
      // Retry fetch if failed
      _loading = true;
      setState((){});
      _fetchData().then((_){
         setState(() => _loading = false);
         if(_data != null) _revealAnim();
         else ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("Connection Error")));
      });
    } else {
      _revealAnim();
    }
  }

  void _revealAnim() {
    setState(() => _state = 'revealed');
  }

  void _reset() {
    setState(() {
      _state = 'deck';
      _selectedIndices = [];
      _data = null; 
    });
    _fetchData(); // Pre-fetch for next round
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: BackButton(color: Colors.white),
        title: Text(widget.lang == 'tr' ? "Mistik Tarot" : "Mystic Tarot",
          style: const TextStyle(color: Color(0xFFFFD700), fontWeight: FontWeight.bold, fontSize: 24),
        ),
        centerTitle: true,
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: RadialGradient(
            center: Alignment.center,
            radius: 1.5,
            colors: [Color(0xFF1a0b2e), Color(0xFF0F0C29)],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              // Header Hint
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                child: Text(
                  widget.lang == 'tr' 
                    ? (_state == 'deck' ? "Kartlara odaklan ve dokun..." : _state == 'spread' && _selectedIndices.length < 3 ? "3 Kart Seç (${_selectedIndices.length}/3)" : _state == 'revealed' ? "Kaderin Çizildi" : "Kaderini Göster")
                    : (_state == 'deck' ? "Focus and tap the deck..." : _state == 'spread' && _selectedIndices.length < 3 ? "Pick 3 Cards (${_selectedIndices.length}/3)" : _state == 'revealed' ? "Your Destiny Awaits" : "Reveal Destiny"),
                  style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 16),
                  textAlign: TextAlign.center,
                ).animate().fadeIn(),
              ),

              Expanded(
                child: _state == 'revealed' ? _buildRevealedView() : _buildInteractiveView(),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildInteractiveView() {
    return Column(
      children: [
        Expanded(
          child: _state == 'deck' 
            ? Center(
                child: _error != null 
                ? Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text("Error Loading Cards", style: TextStyle(color: Colors.redAccent, fontSize: 18)),
                      const SizedBox(height: 10),
                      Text(_error!, style: TextStyle(color: Colors.white54, fontSize: 10), textAlign: TextAlign.center),
                      const SizedBox(height: 10),
                      ElevatedButton(onPressed: _fetchData, child: const Text("Retry"))
                    ],
                  )
                : MouseRegion(
                    cursor: SystemMouseCursors.click,
                    child: GestureDetector(
                      onTap: _startSpread,
                      child: Container(
                        width: 120, height: 200,
                        decoration: BoxDecoration(
                          color: const Color(0xFF222244),
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: Colors.amber.withOpacity(0.5), width: 2),
                          boxShadow: [BoxShadow(color: Colors.black54, blurRadius: 20)],
                        ),
                        child: const Center(child: Text("?", style: TextStyle(color: Colors.amber, fontSize: 40))),
                      ).animate(onPlay: (c)=>c.repeat(reverse:true)).scale(begin: Offset(1,1), end: Offset(1.05, 1.05), duration: 1500.ms),
                    ),
                  ),
              )
            : Stack(
                children: [
                  // --- SIMPLE GRID SPREAD ---
                  GridView.builder(
                    padding: const EdgeInsets.all(20),
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 4, // 4 cards per row
                      childAspectRatio: 0.7,
                      crossAxisSpacing: 10,
                      mainAxisSpacing: 10,
                    ),
                    itemCount: _totalCards,
                    itemBuilder: (context, i) {
                      if (_selectedIndices.contains(i)) {
                        return const SizedBox.shrink(); // Hide picked cards
                      }
                      return GestureDetector(
                        onTap: () => _selectCard(i),
                        child: Container(
                          decoration: BoxDecoration(
                            color: const Color(0xFF222244),
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: Colors.white24),
                            boxShadow: [BoxShadow(color: Colors.black45, blurRadius: 2)],
                          ),
                          child: const Center(child: Icon(Icons.star, size: 12, color: Colors.white12)),
                        ),
                      ).animate().fadeIn(delay: (i * 30).ms);
                    },
                  ),

                  // --- REVEAL BUTTON ---
                  if (_state == 'spread' && _selectedIndices.length == 3)
                    Positioned(
                      bottom: 20, left: 0, right: 0,
                      child: Center(
                        child: ElevatedButton.icon(
                          icon: _loading ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2)) : const Icon(Icons.auto_awesome),
                          label: Text(widget.lang == 'tr' ? "KADERİNİ GÖSTER" : "REVEAL DESTINY"),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: const Color(0xFFFFD700),
                            foregroundColor: Colors.black,
                            padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                            textStyle: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                          ),
                          onPressed: _loading ? null : _reveal,
                        ).animate().scale(duration: 300.ms, curve: Curves.elasticOut),
                      ),
                    ),
                ],
              ),
        ),

        // --- SLOTS AREA ---
        SizedBox(
          height: 180, // Reduced height for better fit
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: List.generate(3, (index) {
              final isFilled = index < _selectedIndices.length;
              return _buildSlot(index, isFilled, null);
            }),
          ),
        ),
        const SizedBox(height: 10),
      ],
    );
  }


  Widget _buildRevealedView() {
    if(_data == null) return const Center(child: CircularProgressIndicator());
    final wish = _data!.wish;
    final color = wish.score >= 0 ? Colors.amber : Colors.redAccent;
    
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        // 1. CARDS ROW
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: List.generate(3, (index) => _buildSlot(index, true, _data!.cards[index])),
        ),
        const SizedBox(height: 30),
        
        // 2. SYNTHESIS CARD
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            border: Border.all(color: color.withOpacity(0.5)),
            borderRadius: BorderRadius.circular(16),
            color: color.withOpacity(0.1),
          ),
          child: Column(
            children: [
              Text(wish.title, style: TextStyle(color: color, fontSize: 22, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
              const SizedBox(height: 10),
              Text(wish.text, style: const TextStyle(color: Colors.white, fontSize: 16, fontStyle: FontStyle.italic), textAlign: TextAlign.center),
              const Divider(color: Colors.white24, height: 30),
              Text(widget.lang == 'tr' ? "Kozmik Özet" : "Cosmic Synthesis", style: const TextStyle(color: Colors.white54, fontSize: 12, letterSpacing: 2)),
              const SizedBox(height: 10),
              Text(_data!.synthesis, style: const TextStyle(color: Colors.white, fontSize: 16, height: 1.5), textAlign: TextAlign.justify),
            ],
          ),
        ).animate().fadeIn(delay: 500.ms).slideY(begin: 0.1, end: 0),
        
        const SizedBox(height: 30),
        
        // 3. DETAILED INTERPRETATIONS
         ..._data!.cards.map((c) => Container(
            margin: const EdgeInsets.only(bottom: 15),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.05),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.white10),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(c.element == 'Fire' ? '🔥' : c.element == 'Water' ? '💧' : c.element == 'Air' ? '🌪️' : '🌿', style: const TextStyle(fontSize: 24)),
                    const SizedBox(width: 10),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(c.position, style: TextStyle(color: HexColor.fromHex(c.color), fontWeight: FontWeight.bold)),
                        Text("${c.name} ${c.isReversed ? '(Rev)' : ''}", style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                      ],
                    )
                  ],
                ),
                const SizedBox(height: 10),
                Text(c.meaning, style: const TextStyle(color: Colors.white70, fontSize: 14, height: 1.5)),
              ],
            ),
         )).toList().animate(interval: 200.ms).fadeIn(),

         const SizedBox(height: 30),
         Center(
           child: ElevatedButton.icon(
             icon: const Icon(Icons.refresh),
             label: Text(widget.lang == 'tr' ? "TEKRAR ÇEK" : "NEW READING"),
             style: ElevatedButton.styleFrom(backgroundColor: Colors.white10, foregroundColor: Colors.white),
             onPressed: _reset,
           ),
         ),
         const SizedBox(height: 50),
      ],
    );
  }

  Widget _buildSlot(int index, bool isFilled, TarotCard? card) {
    if (!isFilled) {
      // Empty Slot
      return Container(
        width: 100, height: 170,
        decoration: BoxDecoration(
          border: Border.all(color: Colors.white24, style: BorderStyle.solid),
          borderRadius: BorderRadius.circular(12),
          color: Colors.white.withOpacity(0.05)
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(index == 0 ? "PAST" : index == 1 ? "PRESENT" : "FUTURE", style: const TextStyle(color: Colors.white54, fontSize: 10)),
            Icon(index == 0 ? Icons.history : index == 1 ? Icons.hourglass_empty : Icons.rocket_launch, color: Colors.white24),
          ],
        ),
      );
    } else {
      // Filled Card
      Widget child = Container(
        width: 100, height: 170,
        decoration: BoxDecoration(
          color: card == null ? const Color(0xFF222244) : Colors.white,
          borderRadius: BorderRadius.circular(12),
          boxShadow: [const BoxShadow(color: Colors.black54, blurRadius: 10)],
        ),
         child: card == null 
           ? const Center(child: Icon(Icons.star, color: Colors.amber)) // Card Back
           : _buildFront(card), // Card Front
      );

      if (card != null) {
         return child.animate().flip(duration: 600.ms);
      }
      return child;
    }
  }

  Widget _buildFront(TarotCard card) {
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: const Color(0xFFF5F5DC), // Beige paper
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFFFD700), width: 2),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(card.name, textAlign: TextAlign.center, style: GoogleFonts.cinzel(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.black87)),
          
          Expanded(child: Center(child: Text(
            card.element == 'Fire' ? '🔥' : card.element == 'Water' ? '💧' : card.element == 'Air' ? '🌪️' : '🌿',
            style: const TextStyle(fontSize: 40),
          ))),
          
          if(card.isReversed)
             const Text("REVERSED", style: TextStyle(color: Colors.red, fontSize: 8, fontWeight: FontWeight.bold)),
             
          Text(card.position, style: const TextStyle(color: Colors.grey, fontSize: 8)),
        ],
      ),
    );
  }
}

class HexColor {
  static Color fromHex(String hexString) {
    final buffer = StringBuffer();
    if (hexString.length == 6 || hexString.length == 7) buffer.write('ff');
    buffer.write(hexString.replaceFirst('#', ''));
    return Color(int.parse(buffer.toString(), radix: 16));
  }
}
