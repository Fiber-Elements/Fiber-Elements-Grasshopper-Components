import Rhino
import scriptcontext as sc
import Grasshopper as gh
import System

def unroll_brep_with_points(brep, points):
    """Unrolls a Brep while strictly maintaining the original point indices."""
    # Ensure Brep is valid
    if isinstance(brep, gh.Kernel.Types.GH_Brep):
        brep = brep.Value  
    if not isinstance(brep, Rhino.Geometry.Brep) or not brep.IsValid:
        print("❌ Invalid Brep")
        return None, None
        
    # Process input points
    original_points = []
    
    for i, pt in enumerate(points):
        # Convert to Point3d if needed
        if isinstance(pt, gh.Kernel.Types.GH_Point):
            pt_value = pt.Value
        elif isinstance(pt, Rhino.Geometry.Point3d):
            pt_value = pt
        else:
            print(f"⚠️ Skipping point {i} - invalid type: {type(pt)}")
            continue
            
        # Store index and point
        original_points.append((i, pt_value))
    
    print(f"✅ Input Points: {len(original_points)}")
    
    # Create a separate unroller for each point
    # This guarantees independent tracking without conflicts
    unrolled_points = [None] * len(original_points)
    
    for idx, point in original_points:
        # Create a new unroller for this point only
        unroller = Rhino.Geometry.Unroller(brep)
        
        # Add just this point to follow
        unroller.AddFollowingGeometry(point)
        
        # Perform the unrolling
        unroll_result = unroller.PerformUnroll()
        
        if not unroll_result or len(unroll_result) < 1:
            print(f"⚠️ Unrolling failed for point {idx}")
            continue
        
        # Get the unrolled point
        unrolled_geometries = unroll_result[2]  # Points come back in 3rd tuple element
        
        if unrolled_geometries and len(unrolled_geometries) > 0:
            # Store the unrolled point at its original index
            unrolled_points[idx] = unrolled_geometries[0]
        else:
            print(f"⚠️ No unrolled result for point {idx}")
    
    # Get the unrolled brep (using a separate unroller)
    brep_unroller = Rhino.Geometry.Unroller(brep)
    brep_result = brep_unroller.PerformUnroll()
    
    if not brep_result or len(brep_result) < 1 or len(brep_result[0]) < 1:
        print("❌ Brep unrolling failed")
        return None, unrolled_points
    
    unrolled_breps = brep_result[0]
    
    # Check for any missing points
    missing = [i for i, pt in enumerate(unrolled_points) if pt is None]
    if missing:
        print(f"⚠️ Warning: {len(missing)} points could not be mapped: {missing}")
    else:
        print("✅ All points successfully mapped")
    
    return unrolled_breps, unrolled_points

# Grasshopper Inputs
brep_input = B  
points_input = P  

# Ensure points are in a list
if not isinstance(points_input, list):
    points_input = [points_input]

# Run function
U, T = unroll_brep_with_points(brep_input, points_input)