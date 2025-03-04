# Grasshopper Brep Unroller with Index Preservation

## Overview

This Grasshopper Python component unrolls a Brep surface while preserving the exact order of point indices. Unlike standard unrolling components that may reorder points during the unrolling process, this script guarantees that each point maintains its original index position in the output.

## Purpose

When working with parametric surfaces in digital fabrication, architectural design, or computational geometry, preserving the order of points during surface unrolling is often critical:

- Maintaining correspondence between 3D design and 2D fabrication
- Preserving numbering systems for assembly instructions
- Ensuring accurate point-to-point mapping for data visualization
- Maintaining alignment with external data sources

## How It Works

The component uses a point-by-point unrolling strategy:

1. Each input point is processed independently with its own dedicated unroller
2. Points are tracked throughout the unrolling process
3. Results are carefully placed back at their original indices
4. The Brep is unrolled separately to avoid interference

This approach guarantees index preservation at the cost of slightly increased computation time.

## Inputs

- **B**: The Brep surface to unroll (must be developable)
- **P**: A list of points to unroll along with the surface

## Outputs

- **U**: The unrolled Brep surface(s)
- **T**: The unrolled points, maintaining their original indices

## Usage Notes

- The Brep should be a developable surface for best results
- Points should lie on or very near the Brep surface
- Performance scales linearly with the number of input points
- For large point sets, computation time may increase notably

## Example Applications

- Unrolling curved panel layouts for fabrication
- Mapping data points from 3D to 2D while preserving relationships
- Creating precise cutting patterns for curved surfaces
- Generating accurate 2D representations of 3D parametric designs

## Technical Details

The component overcomes limitations in the standard Rhino Unroller class by:
- Isolating each point to prevent cross-interference
- Avoiding reliance on face mappings that may change during unrolling
- Using independent unrolling operations to guarantee index preservation
- Implementing error checking and reporting for validation

## Requirements

- Rhinoceros 7 or higher
- Grasshopper
- Python 3 component (GhPython)

## Performance Considerations

This approach prioritizes accuracy over speed. For extremely large point sets (100+), consider:
- Batching points into smaller groups
- Simplifying the Brep if possible
- Running as a background process if available

## Troubleshooting

If points don't unroll correctly:
- Ensure all points lie on or very close to the Brep surface
- Check that the Brep is developable (can be flattened without distortion)
- Verify that the Brep has a valid topology without naked edges
- Inspect the script output for specific error messages
