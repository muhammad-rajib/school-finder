import type { PropsWithChildren } from "react";

type ContainerProps = PropsWithChildren<{
  className?: string;
  as?: "div" | "section";
}>;

export function Container({ children, className = "", as = "div" }: ContainerProps) {
  const Component = as;
  const classes = ["container", className].filter(Boolean).join(" ");

  return <Component className={classes}>{children}</Component>;
}
