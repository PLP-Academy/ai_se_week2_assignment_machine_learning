#!/usr/bin/env python3
"""
AI for Sustainable Cities - Presentation Launcher
Opens the HTML presentation in the default web browser
"""

import webbrowser
import os
import sys
from pathlib import Path

def launch_presentation():
    """Launch the HTML presentation in the default web browser."""

    # Get the current directory
    current_dir = Path(__file__).parent
    presentation_file = current_dir / "project_presentation.html"

    if not presentation_file.exists():
        print("❌ Error: project_presentation.html not found!")
        print(f"Expected location: {presentation_file}")
        print("\nPlease ensure you are running this from the project directory.")
        return False

    # Convert path to file URL
    file_url = f"file://{presentation_file.absolute()}"

    print("🚀 Launching AI for Sustainable Cities Presentation...")
    print("=" * 60)
    print(f"📁 Presentation file: {presentation_file}")
    print(f"🌐 Opening in browser: {file_url}")
    print("\n✨ Features included:")
    print("  🎨 Beautiful responsive design")
    print("  📊 Dynamic data visualization")
    print("  🖼️  Embedded project images")
    print("  🎯 Interactive navigation")
    print("  ⌨️  Keyboard controls (arrow keys)")
    print("  📱 Mobile-friendly layout")
    print("  🤖 AI-powered content sections")

    try:
        # Open in default browser
        webbrowser.open(file_url)
        print("\n✅ Presentation launched successfully!")
        print("🎉 Open your web browser to view the presentation")
        print("\n💡 Tips:")
        print("  • Use arrow keys to navigate between slides")
        print("  • Click navigation dots on the right")
        print("  • Scroll to advance through content")
        print("  • Click 'Launch Interactive Dashboard' to explore live analysis")

        return True

    except Exception as e:
        print(f"\n❌ Error launching presentation: {e}")
        print("\n🔧 Alternative: Open project_presentation.html manually in your browser")
        return False

def check_prerequisites():
    """Check if all required files are present."""

    current_dir = Path(__file__).parent

    required_files = [
        "project_presentation.html",
        "figures/pca_clusters.png",
        "figures/feature_means_by_cluster.png",
        "figures/histograms.png",
        "figures/correlation_heatmap.png",
        "figures/scatter_matrix.png",
        "figures/plotly_pca_clusters.html"
    ]

    missing_files = []

    for file_path in required_files:
        full_path = current_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)

    if missing_files:
        print("⚠️  Warning: Some presentation files are missing:")
        for file in missing_files:
            print(f"   • {file}")
        print("\nThe presentation may not display all images correctly.")
        print("Run the data analysis notebook first to generate all figures.")
        return False

    return True

if __name__ == "__main__":
    print("🤖 AI for Sustainable Cities - Presentation Launcher")
    print("=" * 60)

    # Check prerequisites
    files_ok = check_prerequisites()

    if files_ok:
        print("\n✅ All presentation files found!")
    else:
        print("\n⚠️  Some files missing - presentation may have limited functionality")

    print("\n" + "=" * 60)

    # Launch presentation
    success = launch_presentation()

    if success:
        print("\n🎊 Happy presenting!")
        print("Share your AI-powered urban analysis with the world! 🌍✨")
    else:
        sys.exit(1)
