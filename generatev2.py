import os
import math
import pandas as pd
# ----------------CHANGE THIS CHANGE THIS CHANGE THOS -------------------
df = pd.read_csv('data.csv')
# ----------------CHANGE THIS CHANGE THIS CHANGE THOS -------------------

# Define your base TeX template
base_template = r"""
\documentclass[12pt, letterpaper]{article}
\usepackage{graphicx}
\graphicspath{{Images/}}
\usepackage{subcaption}
\usepackage[left=10mm,right=10mm,top=5mm,bottom=5mm,paper=a4paper]{geometry}
\usepackage{multirow}
\usepackage{caption}  % Added for \captionof
\usepackage{xcolor}
\usepackage{fontspec}
\setmainfont{Tahoma}
\usepackage[utf8]{inputenc}

\setlength{\fboxsep}{0pt} % <-- Add this line
\captionsetup[subfigure]{labelformat=empty}

\begin{document}
"""

# Define the section template to be added
section_template = r"""
\begin{figure}[h]
	\centering
	\fbox{\parbox{1\linewidth}{
	\vspace{5mm}
			\begin{subfigure}{\linewidth}
				\centering
				\includegraphics[height=0.37\textheight]{#photopath1#}
				\caption{#CAPTION1# #title1# - #comment1#}
				%\label{fig:dragon1}
			\end{subfigure}

			\vspace{\baselineskip}

            \begin{subfigure}{\linewidth}
				\centering
				\includegraphics[height=0.37\textheight]{#photopath2#}
				\caption{#CAPTION2# #title2# - #comment2#}
				%\label{fig:dragon1}
			\end{subfigure}

			\vspace{\baselineskip}

			\hrule
			 \begin{minipage}[c][3.5cm][t]{0.4\textwidth} % Larger Left side
			        %\centering
				\begin{minipage}[t][1.5cm][t]{0.4\textwidth} % Set explicit width for Right top
				\vspace{2mm}
				\hspace{2mm}
				    \raggedright
				    \textbf{\small{Notes:} \footnotesize{}}

				\end{minipage}
				 \hrule
			            \begin{minipage}[c][2cm][c]{\textwidth} % Adjust height and alignment
				    \centering
			                \includegraphics[height=1.8cm]{P:/Tools/DocumentGeneration/gwp.png}
			            \end{minipage}
			    \end{minipage}%
			    \vline % Vertical line
			    \begin{minipage}[c][3cm][t]{0.6\textwidth} % Larger Right side with no indentation
			        \begin{minipage}[c][1cm][t]{0.6\textwidth} % Set explicit width for Right top
				\vspace{2mm}     
				\hspace{2mm}
				    \raggedright
				\textbf{\small{Client:} \footnotesize{}} 
			        \end{minipage}
			        \hrule % Horizontal line
			        \begin{minipage}[c][1.4cm][t]{0.6\textwidth} % Set explicit width for Right bottom
				\vspace{2mm}
				\hspace{2mm}
				    \raggedright
				 \textbf{\small{Project:} \footnotesize{}} 
			        \end{minipage}
			        \hrule % Horizontal line
			        \begin{minipage}[c][0.6cm][t]{0.6\textwidth} % Set explicit width for Right bottom    
				\vspace{2mm}
				\hspace{2mm}
				    \raggedright
				\textbf{\footnotesize Appendix:} 
			        \end{minipage}
			    \end{minipage}
			
		}}
\end{figure}
"""

# --------------------------------------------------------------------------------------------------------------------
result = math.ceil(len(df) / 2)

df.sort_values(by='OBJECTID')
result_df = df[['PTName', 'Comment', 'OBJECTID']]
result_df['photonum'] = range(1, len(result_df) + 1)

# Check if the number of images is odd
if len(result_df) % 2 == 1:
    # Duplicate the last row
    last_row = result_df.iloc[-1].copy()
    last_row['OBJECTID'] += 1
    last_row['photonum'] += 1
    result_df = pd.concat([result_df, pd.DataFrame([last_row])], ignore_index=True)
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Build the TeX content by replacing # LOOP_SECTION # with the section template within a loop
photo=1

tex_content = base_template
for i in range(result):
    caption1 = f"Photo {photo}:"
    caption2 = f"Photo {photo+1}:"

    filtered=result_df['photonum'] == photo
    title1 = result_df.loc[filtered, 'PTName'].iloc[0]
    comment1 = result_df.loc[filtered, 'Comment'].iloc[0]
    photopath1 = (result_df.loc[filtered, 'PTName'].iloc[0] + '.jpg')
    photo+=1

    filtered2=result_df['photonum'] == photo
    title2 = result_df.loc[filtered2, 'PTName'].iloc[0]
    comment2 = result_df.loc[filtered2, 'Comment'].iloc[0]
    photopath2 = (result_df.loc[filtered2, 'PTName'].iloc[0] + '.jpg')
    photo+=1

    section_content = section_template.replace("#CAPTION1#", caption1).replace("#photopath1#", photopath1).replace("#title1#", str(title1)).replace("#comment1#", str(comment1)).replace("#CAPTION2#", caption2).replace("#photopath2#", photopath2).replace("#title2#", str(title2)).replace("#comment2#", str(comment2))
    tex_content += section_content

tex_content += r"\end{document}"

# Write the generated TeX content to a file
with open("output.tex", "w") as tex_file:
    tex_file.write(tex_content)
