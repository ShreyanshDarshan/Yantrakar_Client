#include <wx/wx.h>
#include <wx/grid.h>
#include <iostream>

using namespace std;

const char* images[6] = {"test.png", "Capture.png", "wxOutput.png", "test1.png" , "test2.png" , "test3.png" };

class MainFrame : public wxFrame
{
public:
    MainFrame(const wxString& title);

};

class MyApp : public wxApp
{
public:
    virtual bool OnInit();
};

MainFrame::MainFrame(const wxString& title)
    : wxFrame(NULL, wxID_ANY, title, wxDefaultPosition, wxSize(750, 750), wxDEFAULT_FRAME_STYLE & ~(wxRESIZE_BORDER | wxMAXIMIZE_BOX))
{
    wxImage::AddHandler(new wxPNGHandler());
    SetFont(wxFont(15, wxFONTFAMILY_SWISS, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_NORMAL));
    wxPanel* panel = new wxPanel(this, -1, wxPoint(0, 0), wxSize(750, 750));
       
    wxStaticText* cameraIDLabel = new wxStaticText(panel, wxID_ANY, wxString("Camera ID"), wxPoint(50, 40), wxSize(100, 40));
    wxComboBox* cameraIDEntry = new wxComboBox(panel, wxID_ANY, wxString(""), wxPoint(180, 37), wxSize(200, 40));
    //cameraIDEntry->Append(wxString("camera#1"));
    //cameraIDEntry->Append(wxString("camera#2"));
    //cameraIDEntry->Append(wxString("camera#3"));

    wxButton* viewButton = new wxButton(panel, wxID_ANY, wxString("View"), wxPoint(400, 32), wxSize(100, 40));
    viewButton->SetBackgroundColour(wxColor(*wxWHITE));

    
    wxPanel* detailsPanel = new wxPanel(panel, wxID_ANY, wxPoint(50, 100), wxSize(650, 570));
    detailsPanel->SetBackgroundColour(wxColor(227, 230, 228));
    wxFlexGridSizer* detailsPanelGrid = new wxFlexGridSizer(2, 10, 10);
    

    for (int i = 0; i < 6; i++)
    {
        wxImage *img = new wxImage(images[i], wxBITMAP_TYPE_ANY);
        wxImage img2 = img->Scale(315, 250);
        wxStaticBitmap *sbi = new wxStaticBitmap(detailsPanel, -1, wxBitmap(img2));

        detailsPanelGrid->Add(sbi);
    }

    detailsPanelGrid->SetDimension(wxPoint(0, 0), wxSize(650, 570));
    detailsPanel->SetContainingSizer(detailsPanelGrid);

    //wxBitmap* img = new wxBitmap("test.png", wxBITMAP_TYPE_ANY);
    //wxImage* img = new wxImage("test.png", wxBITMAP_TYPE_ANY);
    //img->LoadFile("./test.PNG", wxBITMAP_TYPE_ANY);

    Centre();
    SetBackgroundColour(wxColour(*wxWHITE));
}

IMPLEMENT_APP(MyApp)

bool MyApp::OnInit()
{
    MainFrame* frame = new MainFrame(wxT("Yantrakar Client"));
    frame->Show(true);

    return true;
}