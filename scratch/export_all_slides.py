import os
import subprocess

os.makedirs(r"scratch\slide_images", exist_ok=True)

slides = [
    ("slide_01_p2_arch.png", "p2"),
    ("slide_02_p3_patterns.png", "p3"),
    ("slide_03_p4_decorator_uml.png", "p4"),
    ("slide_04_p5_decorator_pipeline.png", "p5"),
    ("slide_05_p6_composite_uml.png", "p6"),
    ("slide_06_p7_composite_tree.png", "p7"),
    ("slide_07_p8_chain_uml.png", "p8"),
    ("slide_08_p9_chain_flow.png", "p9"),
    ("slide_09_p10_flyweight_uml.png", "p10"),
    ("slide_10_p11_flyweight_memory.png", "p11"),
    ("slide_11_p12_interpreter_uml.png", "p12"),
    ("slide_12_p13_interpreter_ast.png", "p13"),
    ("slide_13_p14_use_case.png", "p14"),
    ("slide_14_p15_sequence.png", "p15"),
    ("slide_15_p16_database.png", "p16"),
]

for filename, slide_id in slides:
    out_path = os.path.join(r"scratch\slide_images", filename)
    cmd = f'gslides readonly export-thumbnail 1GAkU-MICbwrZLl8UaIKNKnfmZv0yNGVoG1s27p-lChA "{out_path}" --slide {slide_id}'
    print(f"Exporting {slide_id} -> {filename}...")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error exporting {slide_id}: {res.stderr}")
    else:
        print(f"Exported {filename} successfully ({os.path.getsize(out_path)} bytes)")

print("All exports complete!")

