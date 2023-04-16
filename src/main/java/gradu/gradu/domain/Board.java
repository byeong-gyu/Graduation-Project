package gradu.gradu.domain;

import lombok.*;
import org.springframework.web.multipart.MultipartFile;

import javax.persistence.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Entity
@NoArgsConstructor(access= AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
@Getter
public class Board {

    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="board_id")
    private Long id;

    private String missingName;
    private String missingAge;
    private String missingGender;
    private String missingPlace;
    private String missingDate;
    private LocalDateTime boardTime;

    private int fileAttached;//1이면 첨부, 0이면 없음

    @OneToMany(mappedBy = "board", cascade = CascadeType.REMOVE,orphanRemoval = true)
    private List<BoardFile> boardFileList = new ArrayList<>();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name="member_id")
    private Member member;

    public void setMember(Member member) {
      this.member=member;
      member.getBoards().add(this);
    }
}
