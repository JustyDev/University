(* Lab 2, Part 1: First 10 prime numbers — generation, LSM approximation, error analysis *)

ClearAll["Global`*"];

outputDir = DirectoryName[$InputFileName];
If[outputDir === "", outputDir = NotebookDirectory[] /. $Failed -> Directory[]];

(* ===== 1. Generate first 10 prime numbers =====
   Required commands: Do, If, IntegerQ, AppendTo, Complement *)

primeList  = {};
candidates = {};

Do[
  AppendTo[candidates, n];
  divisors = {};
  Do[
    If[IntegerQ[n/k], AppendTo[divisors, k]],
    {k, 2, n - 1}
  ];
  (* Complement[divisors, {}] == {} iff no proper divisors exist -> n is prime *)
  If[Complement[divisors, {}] === {}, AppendTo[primeList, n]];
  If[Length[primeList] >= 10, Break[]],
  {n, 2, 100}
];

Print["First 10 prime numbers: ", primeList];

(* ===== 2. Build data points and fit quadratic polynomial by LSM ===== *)

xValues = Range[Length[primeList]];
points  = Transpose[{xValues, primeList}];

fitModel    = Fit[points, {1, x, x^2}, x];
approxValues = Table[fitModel /. x -> i, {i, xValues}];
errors       = N[primeList - approxValues];

maxError = Max[Abs[errors]];
n        = Length[primeList];
mse      = N[(1/n) Total[errors^2]];
mae      = N[(1/n) Total[Abs[errors]]];

Print["Quadratic approximation: y = ", fitModel // InputForm];
Print["Approximation values: ", approxValues // N];
Print["Residuals (Yi - Yhat_i): ", errors];
Print["Max absolute error: ", maxError // N];
Print["MSE = ", mse];
Print["MAE = ", mae];

(* ===== 3. Plots ===== *)

primePlot = ListPlot[
  points,
  Joined        -> True,
  PlotStyle     -> Directive[Blue, Thickness[0.005]],
  PlotMarkers   -> {Automatic, Medium},
  PlotLegends   -> Placed[{"\:041f\:0440\:043e\:0441\:0442\:044b\:0435 \:0447\:0438\:0441\:043b\:0430"}, {Right, Top}],
  PlotLabel     -> "\:041f\:0440\:043e\:0441\:0442\:044b\:0435 \:0447\:0438\:0441\:043b\:0430",
  AxesLabel     -> {"x", "y"},
  AxesOrigin    -> {0, 0},
  ImageSize     -> Large
];

approxPlot = Plot[
  fitModel,
  {x, 1, 10},
  PlotStyle   -> Directive[Orange, Thickness[0.005]],
  PlotLegends -> Placed[{"\:0410\:043f\:043f\:0440\:043e\:043a\:0441\:0438\:043c\:0430\:0446\:0438\:044f \:0440\:044f\:0434\:0430 \:043f\:0440\:043e\:0441\:0442\:044b\:0445 \:0447\:0438\:0441\:0435\:043b"}, {Right, Top}]
];

combinedPlot = Show[
  primePlot,
  approxPlot,
  PlotRange  -> All,
  ImagePadding -> 30
];

(* Error curve: |Yi - Yhat_i| plotted at each index *)
errorPoints = Transpose[{xValues, Abs[errors]}];
errorPlot = ListPlot[
  errorPoints,
  Joined      -> True,
  PlotStyle   -> Directive[Darker[Red], Thickness[0.005]],
  PlotMarkers -> {Automatic, Medium},
  PlotLegends -> Placed[{"\:041e\:0448\:0438\:0431\:043a\:0430 \:0430\:043f\:043f\:0440\:043e\:043a\:0441\:0438\:043c\:0430\:0446\:0438\:0438"}, {Right, Top}]
];

(* Figure 1: original data + approximation + error on one plot *)
figure1 = Show[
  combinedPlot,
  errorPlot,
  PlotRange  -> All,
  PlotLabel  -> "\:041f\:0440\:043e\:0441\:0442\:044b\:0435 \:0447\:0438\:0441\:043b\:0430",
  AxesLabel  -> {"x", "y"},
  AxesOrigin -> {0, 0},
  ImagePadding -> 30
];

figure1

(* ===== 4. Export ===== *)

Export[FileNameJoin[{outputDir, "combined_plot.png"}],    combinedPlot];
Export[FileNameJoin[{outputDir, "figure1_with_error.png"}], figure1];

reportText = StringRiffle[
  {
    "First 10 prime numbers: "      <> ToString[primeList],
    "Quadratic approximation: y = " <> ToString[fitModel // InputForm],
    "Approximation values: "        <> ToString[N[approxValues]],
    "Residuals (Yi - Yhat_i): "     <> ToString[errors],
    "Max absolute error: "          <> ToString[N[maxError]],
    "MSE = "                        <> ToString[mse],
    "MAE = "                        <> ToString[mae]
  },
  "\n"
];

Export[FileNameJoin[{outputDir, "lab2_results.txt"}], reportText, "Text"];

Print["Done. Figures and results saved to ", outputDir];
