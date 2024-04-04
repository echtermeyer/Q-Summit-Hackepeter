import * as React from "react";
import * as ProgressPrimitive from "@radix-ui/react-progress";

import { cn } from "@/lib/utils";

// Define a type for the props expected by the Progress component,
// including any custom props you might need.
interface ProgressProps extends React.ComponentPropsWithoutRef<typeof ProgressPrimitive.Root> {
  value: number; // Ensure `value` is always expected to be a number
  className?: string; // Optional className string
}

// Helper function to determine the color class based on the value
function getProgressColor(value: number): string {
  if (value === 5) return "bg-dark-green";
  if (value === 4) return "bg-light-green";
  if (value === 3) return "bg-yellow";
  if (value === 2) return "bg-orange";
  return "bg-red";
}

const Progress = React.forwardRef<React.ElementRef<typeof ProgressPrimitive.Root>, ProgressProps>(
  ({ className, value, ...props }, ref) => (
    <ProgressPrimitive.Root
      ref={ref}
      className={cn("relative h-4 w-full overflow-hidden rounded-full bg-secondary", className)}
      {...props} // Spread the rest of the props to the Root component.
    >
      <ProgressPrimitive.Indicator
        className={cn("h-full w-full flex-1 transition-all", getProgressColor(value))}
        style={{ transform: `translateX(-${100 - value * 20}%)` }} // Assuming value is always provided and is a number
      />
    </ProgressPrimitive.Root>
  )
);

Progress.displayName = "Progress";

export { Progress };
