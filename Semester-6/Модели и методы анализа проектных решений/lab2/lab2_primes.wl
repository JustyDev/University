(* Lab 2, part 1: primes, approximation, and error analysis *)

ClearAll["Global`*"];

outputDir = DirectoryName[$InputFileName];
If[outputDir === "", outputDir = NotebookDirectory[] /. $Failed -> Directory[]];

primeList = {};
candidates = {};

Do[
  AppendTo[candidates, n];
  divisors = {};
  Do[
    If[IntegerQ[N[n/k]] && Mod[n, k] == 0, AppendTo[divisors, k]],
    {k, 2, n - 1}
  ];
  If[Complement[divisors, {}] === {} && n > 1, AppendTo[primeList, n]];
  If[Length[primeList] >= 10, Break[]],
  {n, 2, 100}
];

xValues = Range[Length[primeList]];
points = Transpose[{xValues, primeList}];

fitModel = Fit[points, {1, x, x^2}, x];
approxValues = Table[fitModel /. x -> i, {i, xValues}];
errors = primeList - approxValues;

maxError = Max[Abs[errors]];
mse = N[Mean[errors^2]];
mae = N[Mean[Abs[errors]]];

primePlot = ListPlot[
  points,
  Joined -> True,
  PlotStyle -> Directive[Blue, Thickness[0.006]],
  PlotMarkers -> Automatic,
  PlotLegends -> {"Prime numbers"},
  PlotLabel -> "First 10 Prime Numbers and Quadratic Approximation",
  AxesLabel -> {"Index", "Value"},
  AxesOrigin -> {1, 0},
  ImageSize -> Large
];

approxPlot = Plot[
  fitModel,
  {x, 1, Length[primeList]},
  PlotStyle -> Directive[Red, Thickness[0.006]],
  PlotLegends -> {"Quadratic fit"},
  AxesLabel -> {"Index", "Value"},
  AxesOrigin -> {1, 0},
  ImageSize -> Large
];

combinedPlot = Show[
  primePlot,
  approxPlot,
  PlotRange -> All,
  ImagePadding -> 20
];

errorPoints = Transpose[{xValues, errors}];
errorPlot = ListPlot[
  errorPoints,
  Joined -> True,
  PlotStyle -> Directive[Darker[Green], Thickness[0.006]],
  PlotMarkers -> Automatic,
  PlotLegends -> {"Approximation error"},
  AxesLabel -> {"Index", "Error"},
  AxesOrigin -> {1, 0},
  ImageSize -> Large
];

figure1 = Show[
  combinedPlot,
  errorPlot,
  PlotRange -> All,
  PlotLabel -> "Figure 1. Primes, Quadratic Approximation, and Error",
  ImagePadding -> 20
];

Export[FileNameJoin[{outputDir, "combined_plot.png"}], combinedPlot];
Export[FileNameJoin[{outputDir, "figure1_with_error.png"}], figure1];

reportText = StringRiffle[
  {
    "First 10 prime numbers: " <> ToString[primeList],
    "Points: " <> ToString[points],
    "Quadratic approximation: y = " <> ToString[fitModel // InputForm],
    "Approximation values: " <> ToString[approxValues // N],
    "Errors (Yi - Yhat_i): " <> ToString[errors // N],
    "Maximum absolute error: " <> ToString[N[maxError]],
    "MSE: " <> ToString[mse],
    "MAE: " <> ToString[mae]
  },
  "\n"
];

Export[FileNameJoin[{outputDir, "lab2_results.txt"}], reportText, "Text"];

Print["First 10 prime numbers: ", primeList];
Print["Points: ", points];
Print["Quadratic approximation: y = ", fitModel];
Print["Approximation values: ", N[approxValues]];
Print["Errors (Yi - Yhat_i): ", N[errors]];
Print["Maximum absolute error: ", N[maxError]];
Print["MSE: ", mse];
Print["MAE: ", mae];
Print["Saved files:"];
Print[FileNameJoin[{outputDir, "combined_plot.png"}]];
Print[FileNameJoin[{outputDir, "figure1_with_error.png"}]];
Print[FileNameJoin[{outputDir, "lab2_results.txt"}]];
